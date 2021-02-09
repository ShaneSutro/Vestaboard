import vestaboard
import pytest

validRawChar = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

invalidRawChar = [
    ['t', 't', 't', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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

def test_valid_raw_input_does_not_fail():
    vestaboard.Board().raw(validRawChar)


