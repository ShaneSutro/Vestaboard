import pytest
import vestaboard


def test_enabling_local_api_succeeds(patched_post):
    b = vestaboard.Board(localApi={"enablementToken": "fake", "ip": "10.0.0.1"})
    assert b.localOptions["useSavedToken"] == True


def test_using_manual_key_and_ip():
    b = vestaboard.Board(localApi={"key": "fakeKey", "ip": "10.0.0.1"})
    assert b.localKey == "fakeKey"
    assert b.localIP == "10.0.0.1"


def test_using_saved_key_and_ip(with_token_file):
    b = vestaboard.Board(localApi={"useSavedToken": True})
    assert b.localKey == "fakeLocalKey"
    assert b.localIP == "10.0.0.2"


def test_warns_when_both_key_and_enablement_token(patched_post):
    with pytest.warns(
        UserWarning,
        match="An enablement token was provided, so I'm enabling the local API for you. If you've already enabled the local API on your board, remove the enablement token and try again.",
    ):
        b = vestaboard.Board(
            localApi={"enablementToken": "token", "ip": "10.0.0.1", "key": "fakeKey"}
        )
        assert b.localIP == "10.0.0.1", "Local IP should be the passed-in IP"
        assert (
            b.localKey == "fakelocalkey"
        ), "Should use the new key the board generated"


def test_errors_when_no_ip_provided_to_enable_api():
    with pytest.raises(ValueError):
        vestaboard.Board(localApi={"enablementToken": "token"})


def test_errors_when_no_ip_provided_to_use_api():
    with pytest.raises(ValueError):
        vestaboard.Board(localApi={"key": "token"})


def test_errors_when_no_saved_key_and_none_provided(no_token_file):
    with pytest.raises(ValueError):
        vestaboard.Board(localApi={})


def test_errors_with_save_only(no_token_file):
    with pytest.raises(ValueError):
        vestaboard.Board(localApi={"saveToken": True})


def test_nonexistent_token_file(no_token_file):
    with pytest.raises(FileNotFoundError):
        vestaboard.Board(localApi={"useSavedToken": True})


def test_fails_with_ip_only(no_token_file):
    with pytest.raises(ValueError):
        vestaboard.Board(localApi={"ip": "10.0.0.1"})


def test_should_allow_reading(with_token_file, patched_get):
    b = vestaboard.Board(localApi={"useSavedToken": True})
    chars = b.read()
    assert chars == {
        "message": [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    }


def test_converts_back_into_characters(with_token_file, patched_get):
    b = vestaboard.Board(localApi={"useSavedToken": True})
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


def test_joins_back_into_lines_with_normalize(with_token_file, patched_get):
    b = vestaboard.Board(localApi={"useSavedToken": True})
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

def test_uses_provided_ip_address_when_using_saved_token(with_token_file, patched_get):
    b = vestaboard.Board(localApi={"useSavedToken": True, "ip": "10.10.10.10"})
    assert b.localIP == "10.10.10.10"


