from aoanki.deck import deck_schema_11
from aoanki.deck.deck_schema_11 import NormalDeck,from_json

test_deck_json = """{"1": {"desc": "", "name": "Default", "extendRev": 50, "usn": 0, "collapsed": false, "newToday": [0, 0], "timeToday": [0, 0], "dyn": 0, "extendNew": 10, "conf": 1, "revToday": [0, 0], "lrnToday": [0, 0], "id": 1, "mod": 1374699680}}"""

def test_deck_common_from_dict():
    import json

    decks_dict = json.loads(test_deck_json)

    parsed_decks = {}
    for deck_id, deck_data in decks_dict.items():
        if int(deck_data.get("dyn", 0)) == 1:
            raise ValueError("Dynamic decks are not supported.")
        else:
            parsed_decks[deck_id] = NormalDeck.from_dict(deck_data)
    assert len(parsed_decks) == 1
    assert parsed_decks["1"].common.id == 1
    assert parsed_decks["1"].common.name == "Default"
def test_deck_common_from_json():
    parsed_decks = from_json(test_deck_json)
    assert len(parsed_decks) == 1
    assert parsed_decks["1"].common.id == 1
    assert parsed_decks["1"].common.name == "Default"