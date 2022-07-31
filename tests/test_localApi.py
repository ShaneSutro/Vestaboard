import json
import vestaboard
import pytest
import requests
import os
import json


class MockedResponse:
    def __init__(self):
        def jsonFunc():
            return {"message": "Local API enabled", "apiKey": "fakelocalkey"}

        self.ok = True
        self.json = jsonFunc


@pytest.fixture
def patched_requests(monkeypatch):
    def mocked_post(uri, *args, **kwargs):
        return MockedResponse()

    monkeypatch.setattr(requests, "post", mocked_post)


def test_enabling_local_api_succeeds(patched_requests):
    b = vestaboard.Board(localApi={"enablementToken": "fake", "ip": "10.0.0.1"})
    assert b.localOptions["useSavedToken"] == True


def test_using_manual_key_and_ip():
    b = vestaboard.Board(localApi={"key": "fakeKey", "ip": "10.0.0.1"})
    assert b.localKey == "fakeKey"
    assert b.localIP == "10.0.0.1"


def test_using_saved_key_and_ip():
    create_fake_local_file()
    b = vestaboard.Board(localApi={"useSavedToken": True})
    assert b.localKey == "fakeLocalKey"
    assert b.localIP == "10.0.0.2"
    remove_fake_local_file()


def test_warns_when_both_key_and_enablement_token(patched_requests):
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


def test_errors_when_no_saved_key_and_none_provided():
    with pytest.raises(ValueError):
        remove_fake_local_file()
        vestaboard.Board(localApi={})


def test_errors_with_save_only():
    with pytest.raises(ValueError):
        remove_fake_local_file()
        vestaboard.Board(localApi={"saveToken": True})


def test_nonexistent_token_file():
    with pytest.raises(FileNotFoundError):
        remove_fake_local_file()
        vestaboard.Board(localApi={"useSavedToken": True})


def test_fails_with_ip_only():
    with pytest.raises(ValueError):
        remove_fake_local_file()
        vestaboard.Board(localApi={"ip": "10.0.0.1"})


def create_fake_local_file():
    with open(os.path.dirname(os.path.dirname(__file__)) + "/local.txt", "w") as f:
        f.write("fakeLocalKey\n")
        f.write("10.0.0.2")
        f.close()


def remove_fake_local_file():
    try:
        filePath = os.path.dirname(os.path.dirname(__file__))
        os.remove(filePath + "/local.txt")
    except OSError:
        pass
