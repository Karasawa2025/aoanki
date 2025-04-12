from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union, Any


@dataclass
class TodayAmount:
    day: int = 0
    amount: int = 0

    @staticmethod
    def from_list(v: List[Any]) -> "TodayAmount":
        if isinstance(v, list) and len(v) == 2:
            return TodayAmount(day=int(v[0]), amount=int(v[1]))
        return TodayAmount()


@dataclass
class DeckToday:
    lrn_today: TodayAmount = field(default_factory=TodayAmount)
    rev_today: TodayAmount = field(default_factory=TodayAmount)
    new_today: TodayAmount = field(default_factory=TodayAmount)
    time_today: TodayAmount = field(default_factory=TodayAmount)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DeckToday":
        return DeckToday(
            lrn_today=TodayAmount.from_list(data.get("lrnToday", [0, 0])),
            rev_today=TodayAmount.from_list(data.get("revToday", [0, 0])),
            new_today=TodayAmount.from_list(data.get("newToday", [0, 0])),
            time_today=TodayAmount.from_list(data.get("timeToday", [0, 0])),
        )


@dataclass
class DeckCommon:
    id: int
    name: str
    mtime: int
    usn: int
    study_collapsed: bool = False
    browser_collapsed: bool = False
    desc: str = ""
    markdown_description: bool = False
    dynamic: int = 0
    today: DeckToday = field(default_factory=DeckToday)
    other: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DeckCommon":
        known_keys = {
            "id", "name", "mod", "usn", "collapsed", "browserCollapsed",
            "desc", "md", "dyn", "lrnToday", "revToday", "newToday", "timeToday"
        }

        today = DeckToday.from_dict(data)
        other = {k: v for k, v in data.items() if k not in known_keys}
        return DeckCommon(
            id=int(data["id"]),
            name=data["name"],
            mtime=int(data.get("mod", 0)),
            usn=int(data["usn"]),
            study_collapsed=bool(data.get("collapsed", False)),
            browser_collapsed=bool(data.get("browserCollapsed", False)),
            desc=data.get("desc", ""),
            markdown_description=bool(data.get("md", False)),
            dynamic=int(data.get("dyn", 0)),
            today=today,
            other=other,
        )


@dataclass
class NormalDeck:
    common: DeckCommon
    conf: int
    extend_new: int = 0
    extend_rev: int = 0
    review_limit: Optional[int] = None
    new_limit: Optional[int] = None
    review_limit_today: Optional[List[int]] = None
    new_limit_today: Optional[List[int]] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "NormalDeck":
        common = DeckCommon.from_dict(data)
        return NormalDeck(
            common=common,
            conf=int(data.get("conf", 1)),
            extend_new=int(data.get("extendNew", 0)),
            extend_rev=int(data.get("extendRev", 0)),
            review_limit=data.get("reviewLimit"),
            new_limit=data.get("newLimit"),
            review_limit_today=data.get("reviewLimitToday"),
            new_limit_today=data.get("newLimitToday"),
        )

def from_json(data: str) -> Dict[str, NormalDeck]:
    """
    Convert a JSON string to a NormalDeck object.
    """
    import json
    data_dict = json.loads(data)
    decks = {}
    for deck_id, deck_data in data_dict.items():
        if int(deck_data.get("dyn", 0)) == 1:
            print("Filtered decks not yet supported in this parser.")
        else:
            decks[deck_id] = NormalDeck.from_dict(deck_data)
    return decks


@dataclass
class FilteredSearchTerm:
    search: str
    limit: int
    order: int


@dataclass
class FilteredDeck:
    common: DeckCommon
    resched: bool
    terms: List[FilteredSearchTerm]
    separate: bool = False
    delays: Optional[List[float]] = None
    preview_delay: int = 0
    preview_again_secs: int = 0
    preview_hard_secs: int = 0
    preview_good_secs: int = 0


DeckSchema = Union[NormalDeck, FilteredDeck]
