from aoanki.meta import MetaVersion
import sqlite3
import os


class Database:
    def __init__(self,ankidir):
        self._filename = "collection.anki2" # filename of the database
        self._version = MetaVersion.LEGACY1 # version of the database
        self._card_table = "cards" # table for cards
        self._col_table = "col" # table for collection metadata
        self._grave_table = "graves" # table for graveyard cards
        self._note_table = "notes" # table for notes
        self._revlog_table = "revlog" # table for review logs
        self._db = sqlite3.connect(os.path.join(ankidir,self._filename)) # connect to the database

    def get_cards(self):
        cursor = self._db.cursor()
        cursor.execute(f"SELECT * FROM {self._card_table}")
        cards = cursor.fetchall()
        cursor.close()
        return cards