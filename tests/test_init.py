import vestaboard
import pytest
import os

validRawChar = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

invalidRawChar = [
    ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v'],
    ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v'],
    ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v'],
    ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v'],
    ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v'],
    ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v']
]

def test_installable_with_no_params_errors():
    with pytest.raises(ValueError):
        vestaboard.Installable()

def test_board_instance_fails_with_no_file():
    with pytest.raises(ValueError):
        vestaboard.Board()

def test_raw_input_fails_if_not_a_list():
    with pytest.raises(ValueError):
        vestaboard.Board().raw('not a list')

def test_raw_input_fails_if_not_contains_six_items():
    with pytest.raises(ValueError):
        vestaboard.Board().raw([])

def test_raw_input_fails_if_not_contains_nested_lists():
    with pytest.raises(ValueError):
        vestaboard.Board().raw(['this is a string, not a list'])

def test_raw_input_fails_if_nested_lists_not_contain_22_characters():
    with pytest.raises(ValueError):
        vestaboard.Board().raw([[], [], [], [], [], []])

def test_raw_input_fails_if_nested_lists_not_contain_all_numbers():
    with pytest.raises(ValueError):
        vestaboard.Board().raw(invalidRawChar)

def test_valid_standard_input_does_not_fail():
    create_fake_cred_file()
    vestaboard.Board().post('abcdefghijklmnopqrstuvwxyz1234567890 !@#$()-+&=;:"%,./?°')
    vestaboard.Board().post('Triage Status:\n\n{63}Red - 24 files')
    vestaboard.Board().post('Character code at end {23}')
    vestaboard.Board().post('{64} Character code at beginning')
    remove_fake_cred_file()

def test_invalid_standard_input_fails():
    with pytest.raises(Exception):
        create_fake_cred_file()
        vestaboard.Board().post('^')
        remove_fake_cred_file()

def test_valid_raw_input_does_not_fail():
    create_fake_cred_file()
    vestaboard.Board().raw(validRawChar)
    remove_fake_cred_file()

def test_board_can_be_instantiated_with_an_installable_and_sub_id():
    apiKey = 'fakeApiKey'
    apiSecret = 'fakeApiSecret'
    subId = 'fakeSubId'

    i = vestaboard.Installable(apiKey=apiKey, apiSecret=apiSecret, getSubscription=False, saveCredentials=False)
    vb = vestaboard.Board(i, subscriptionId=subId)
    vb.post('Should not error')

def create_fake_cred_file():
    with open(os.path.dirname(os.path.dirname(__file__)) + '/credentials.txt', 'w') as f:
        f.write('fakeApiKey\n')
        f.write('fakeApiSecre\n')
        f.write('fakeSubscriberId\n')
        f.close()

def remove_fake_cred_file():
    filePath = os.path.dirname(os.path.dirname(__file__))
    os.remove(filePath + '/credentials.txt')