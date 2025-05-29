from __future__ import annotations

import json, os, sqlite3, time, uuid
from aoanki.meta import MetaVersion

DELIM = "\x1f"  # Anki 字段分隔符


class Database:
    def __init__(self, ankidir: str):
        self._filename = "collection.anki2"
        self._version = MetaVersion.LEGACY1
        self._card_table, self._note_table, self._col_table = "cards", "notes", "col"
        self._db = sqlite3.connect(os.path.join(ankidir, self._filename))
        self._db.row_factory = sqlite3.Row

        # ---------- 牌组缓存 ----------
        decks_json = self._db.execute(f"SELECT decks FROM {self._col_table} WHERE id=1").fetchone()["decks"]
        self._decks: dict[str, dict] = json.loads(decks_json)

    # ===== 辅助 =====
    def _save_decks(self):  # 把 self._decks 写回 col
        self._db.execute(
            f"UPDATE {self._col_table} SET decks=? WHERE id=1",
            (json.dumps(self._decks),),
        )
    # ============ 基础信息 ============
    def get_version(self) -> MetaVersion:
        return self._version
    def get_card_all(self):
        return self._db.execute(f"SELECT * FROM {self._card_table}").fetchall()
    def get_note_all(self):
        return self._db.execute(f"SELECT * FROM {self._note_table}").fetchall()
    def get_decks(self):
        return self._decks
    # ============ NOTE 操作 ============
    def get_note(self, nid: int):
        return self._db.execute(f"SELECT * FROM {self._note_table} WHERE id=?", (nid,)).fetchone()

    def add_note(
        self,
        mid: int,
        fields: list[str],
        tags: list[str] | None = None,
        note_id: int | None = None,
    ) -> int:
        """
        创建一条 note（不建卡片）。返回 nid。
        - fields: 按模型顺序给出的字段文字
        - tags: ["tag1", "tag2"] -> "tag1 tag2 "
        """
        note_id = note_id or int(time.time() * 1000)
        now = int(time.time() * 1000)
        sfld = fields[0]
        tags_str = " ".join(tags) + " " if tags else ""
        self._db.execute(
            f"""
            INSERT INTO {self._note_table}
            (id,guid,mid,mod,usn,tags,flds,sfld,csum,flags,data)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                note_id,
                uuid.uuid4().hex,
                mid,
                now,
                -1,
                tags_str,
                DELIM.join(fields),
                sfld,
                0,  # csum 简化：生产环境需 murmurhash3_32(sfld)
                0,
                "",
            ),
        )
        return note_id

    def update_note(self, nid: int, **cols):
        if cols:
            sets = ", ".join(f"{k}=?" for k in cols)
            self._db.execute(f"UPDATE {self._note_table} SET {sets} WHERE id=?", (*cols.values(), nid))

    def delete_note(self, nid: int, cascade: bool = False):
        """若 cascade=True 则同时删除隶属卡片并同步 decks 统计"""
        if cascade:
            # 先找出卡片及其 deck
            cards = self._db.execute(f"SELECT id,did FROM {self._card_table} WHERE nid=?", (nid,)).fetchall()
            for c in cards:
                self.delete_card(c["id"])  # delete_card 会维护 decks 计数
        else:
            # 防御性检查，确保没有卡片后再删
            cnt = self._db.execute(f"SELECT COUNT(*) FROM {self._card_table} WHERE nid=?", (nid,)).fetchone()[0]
            if cnt:
                raise RuntimeError("Note still has cards; use cascade=True")
        self._db.execute(f"DELETE FROM {self._note_table} WHERE id=?", (nid,))

    # ============ CARD 操作（含 decks 更新） ============
    def get_card(self, cid: int):
        return self._db.execute(f"SELECT * FROM {self._card_table} WHERE id=?", (cid,)).fetchone()

    def get_cards_for_note(self, nid: int):
        return self._db.execute(f"SELECT * FROM {self._card_table} WHERE nid=?", (nid,)).fetchall()

    def add_card(
        self,
        nid: int,
        did: int,
        ord_: int,
        queue: int = 0,
        type_: int = 0,
        cid: int | None = None,
    ):
        cid = cid or int(time.time() * 1000)
        now = int(time.time() * 1000)
        self._db.execute(
            f"""
            INSERT INTO {self._card_table}
            (id,nid,did,ord,mod,usn,type,queue,due,ivl,factor,reps,lapses,left,odue,odid,flags,data)
            VALUES(?,?,?,?,?,-1,?,?,?,?,0,0,0,0,0,0,0,'')
            """,
            (cid, nid, did, ord_, now, type_, queue, 0),
        )
        # 更新牌组 newToday 计数
        deck = self._decks.get(str(did))
        if deck:
            today = deck.get("newToday", [int(now / 1000), 0])
            today[1] += 1
            deck["newToday"] = today
            self._save_decks()
        return cid

    def delete_card(self, cid: int):
        card = self.get_card(cid)
        if not card:
            return
        did = card["did"]
        self._db.execute(f"DELETE FROM {self._card_table} WHERE id=?", (cid,))
        # 回写牌组计数
        deck = self._decks.get(str(did))
        if deck:
            today = deck.get("newToday", [int(time.time()), 0])
            today[1] = max(0, today[1] - 1)
            deck["newToday"] = today
            self._save_decks()

    # ============ 高阶联合查询 ============
    def get_card_full(self, cid: int):
        card = self.get_card(cid)
        if not card:
            return None
        note = self.get_note(card["nid"])
        deck_name = self._decks.get(str(card["did"]), {}).get("name", "⍰")
        return {"card": card, "note": note, "deck": deck_name}

    # ============ 批量：一次建 note + 多张 card ============
    def add_note_with_cards(
        self,
        mid: int,
        fields: list[str],
        card_dids: list[int],
        tags: list[str] | None = None,
    ):
        """
        创建一个 note，并为 `card_dids[i]` 在对应牌组建 card(ord=i)。
        返回 (nid, [cid1, cid2, ...])
        """
        try:
            with self._db:
                nid = self.add_note(mid, fields, tags)
                cids = [
                    self.add_card(nid=nid, did=did, ord_=i)
                    for i, did in enumerate(card_dids)
                ]
            return nid, cids
        finally:
            self._db.commit()

    # ============ 关闭 ============
    def close(self):
        self._db.close()
