import pytest
import os
import requests


class MockedResponse:
    def __init__(self):
        def jsonFunc():
            return {"message": "Local API enabled", "apiKey": "fakelocalkey"}

        def raise_for_status():
            return 200

        self.ok = True
        self.json = jsonFunc
        self.raise_for_status = raise_for_status


class MockedRead:
    def __init__(self, response):
        def jsonFunc():
            return response

        def raise_for_status():
            return 200

        self.ok = True
        self.json = jsonFunc
        self.raise_for_status = raise_for_status


def create_fake_cred_file():
    with open(
        os.path.dirname(os.path.dirname(__file__)) + "/credentials.txt", "w"
    ) as f:
        f.write("fakeApiKey\n")
        f.write("fakeApiSecre\n")
        f.write("fakeSubscriberId\n")
        f.close()


def create_fake_token_file():
    with open(os.path.dirname(os.path.dirname(__file__)) + "/local.txt", "w") as f:
        f.write("fakeLocalKey\n")
        f.write("10.0.0.2")
        f.close()


def remove_fake_cred_file(fileName):
    try:
        filePath = os.path.dirname(os.path.dirname(__file__))
        os.remove(filePath + f"/{fileName}.txt")
    except OSError:
        pass


@pytest.fixture
def with_credentials():
    create_fake_cred_file()
    yield True
    remove_fake_cred_file("credentials")


@pytest.fixture
def no_credentials():
    remove_fake_cred_file("credentials")


@pytest.fixture
def with_token_file():
    create_fake_token_file()
    yield True
    remove_fake_cred_file("local")


@pytest.fixture
def no_token_file():
    remove_fake_cred_file("local")


@pytest.fixture
def patched_post(monkeypatch):
    def mocked_post(uri, *args, **kwargs):
        return MockedResponse()

    monkeypatch.setattr(requests, "post", mocked_post)


@pytest.fixture
def patched_get(monkeypatch):
    def mocked_get(uri, *args, **kwargs):
        if uri == "https://rw.vestaboard.com":
            return MockedRead(
                {
                    "currentMessage": {
                        "layout": "[[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]"
                    }
                }
            )
        return MockedRead(
            {
                "message": [
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            }
        )

    monkeypatch.setattr(requests, "get", mocked_get)
