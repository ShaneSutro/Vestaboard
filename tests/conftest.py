import pytest
import os


def create_fake_cred_file():
    with open(
        os.path.dirname(os.path.dirname(__file__)) + "/credentials.txt", "w"
    ) as f:
        f.write("fakeApiKey\n")
        f.write("fakeApiSecre\n")
        f.write("fakeSubscriberId\n")
        f.close()


def remove_fake_cred_file():
    try:
        filePath = os.path.dirname(os.path.dirname(__file__))
        os.remove(filePath + "/credentials.txt")
    except OSError:
        pass


@pytest.fixture
def with_credentials():
    create_fake_cred_file()
    yield True
    remove_fake_cred_file()


@pytest.fixture
def no_credentials():
    remove_fake_cred_file()
