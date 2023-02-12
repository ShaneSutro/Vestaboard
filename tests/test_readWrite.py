import re
import pytest
import vestaboard


def test_instantiating_read_write_board():
    b = vestaboard.Board(apiKey="my read write key", readWrite=True)
    assert b.apiKey == "my read write key", "Should use the passed-in API key"


def test_should_allow_reading(no_credentials, patched_get):
    b = vestaboard.Board(apiKey="my read write key", readWrite=True)
    chars = b.read()
    assert chars == {
        "currentMessage": {
            "layout": "[[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]"
        }
    }


def test_converts_back_into_characters(no_credentials, patched_get):
    b = vestaboard.Board(apiKey="my read write key", readWrite=True)
    chars = b.read({"convert": True})
    # fmt: off
    assert chars == [
                    ['a', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['b', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['c', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['d', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['e', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    ['f', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ]
    # fmt: on


def test_joins_back_into_lines_with_normalize(no_credentials, patched_get):
    b = vestaboard.Board(apiKey="my read write key", readWrite=True)
    chars = b.read({"convert": True, "normalize": True})
    assert (
        chars
        == "a                     \n"
        + "b                     \n"
        + "c                     \n"
        + "d                     \n"
        + "e                     \n"
        + "f                     "
    )


def test_disallows_reading_on_regular_board(with_credentials):
    with pytest.raises(ValueError, match=re.escape('.read() is only available when using local API or by using a read/write enabled API key.\nPass "readWrite=True" along with your apiKey to enable readWrite mode.')):
        b = vestaboard.Board()
        b.read()
