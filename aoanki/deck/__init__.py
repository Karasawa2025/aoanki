from aoanki import note


class Deck:
    id : int
    name : str
    mtime_secs : int
    usn : int
    notes : list[note.Note]