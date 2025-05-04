import vestaboard
import pytest
import os
import re

# fmt: off
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
# fmt: on

TEST_API_KEY = "fakeApiKey"
TEST_API_SECRET = "fakeApiSecret"
TEST_SUB_ID = "fakeSubId"


def test_installable_with_no_params_errors():
    with pytest.raises(
        ValueError, match="Installables must have an apiKey and apiSecret parameter."
    ):
        vestaboard.Installable()


def test_board_instantiation_with_cred_file(with_credentials):
    vestaboard.Board()


def test_installable_with_correct_params():
    i = vestaboard.Installable(TEST_API_KEY, TEST_API_SECRET, False)
    assert i.apiKey == "fakeApiKey"
    assert i.apiSecret == "fakeApiSecret"


def test_board_instance_fails_with_no_file(no_credentials):
    with pytest.raises(
        ValueError,
        match="You must create an installable first or save credentials by passing saveCredentials=True into installable().",
    ):
        vestaboard.Board()


def test_raw_input_fails_if_not_a_list(with_credentials):
    with pytest.raises(
        ValueError, match="Nested items must be lists, not <class 'str'>."
    ):
        vestaboard.Board().raw("not a list")


def test_raw_input_warns_if_not_contains_six_items(with_credentials):
    with pytest.warns(
        UserWarning,
        match='you provided a list with length 0, which has been centered vertically on the board by default. Either provide a list with length 6, or set the "pad" option to suppress this warning.',
    ):
        vestaboard.Board().raw([])


def test_raw_input_fails_if_not_contains_nested_lists(with_credentials):
    with pytest.raises(
        ValueError, match="Nested items must be lists, not <class 'str'>."
    ):
        vestaboard.Board().raw(["this is a string, not a list"])


def test_raw_input_fails_if_nested_lists_not_contain_22_characters(with_credentials):
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Nested lists must be exactly 22 characters long. Element at 0 is 0 characters long. Use the Formatter().convertLine() function if you need to add padding to your row."
        ),
    ):
        vestaboard.Board().raw([[], [], [], [], [], []])


def test_raw_input_fails_if_nested_lists_not_contain_all_numbers(with_credentials):
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Nested lists must contain numbers only - check row 0 char 0 (0 indexed)"
        ),
    ):
        vestaboard.Board().raw(invalidRawChar)


def test_valid_standard_input_does_not_fail(with_credentials, patched_post):
    vestaboard.Board().post('abcdefghijklmnopqrstuvwxyz1234567890 !@#$()-+&=;:"%,./?°')
    vestaboard.Board().post("Triage Status:\n\n{63}Red - 24 files")
    vestaboard.Board().post("Character code at end {23}")
    vestaboard.Board().post("{64} Character code at beginning")


def test_invalid_standard_input_fails(with_credentials):
    with pytest.raises(
        ValueError,
        match="Your text contains one or more characters that the Vestaboard does not support.",
    ):
        vestaboard.Board().post("^")


def test_valid_raw_input_does_not_fail(with_credentials):
    vestaboard.Board().raw(validRawChar)


def test_board_can_be_instantiated_with_an_installable_and_sub_id(patched_post):
    vb = create_fake_vestaboard()
    vb.post("Should not error")


def test_odd_length_center_pad():
    small_board = return_valid_too_small_board()
    vb = create_fake_vestaboard()
    vb.raw(small_board, pad="center")
    expected = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert small_board == expected


def test_even_length_center_pad():
    small_board = return_valid_too_small_board()
    small_board.append(
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    )
    vb = create_fake_vestaboard()
    vb.raw(small_board, pad="center")
    expected = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert small_board == expected


def test_above_pad():
    small_board = return_valid_too_small_board()
    vb = create_fake_vestaboard()
    vb.raw(small_board, pad="above")
    expected = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
    ]
    assert small_board == expected


def test_below_pad():
    small_board = return_valid_too_small_board()
    vb = create_fake_vestaboard()
    vb.raw(small_board, pad="below")
    expected = [
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert small_board == expected


def test_no_pad():
    small_board = return_valid_too_small_board()
    vb = create_fake_vestaboard()
    expected_warning = 'you provided a list with length 3, which has been centered vertically on the board by default. Either provide a list with length 6, or set the "pad" option to suppress this warning.'
    with pytest.warns(UserWarning, match=expected_warning):
        vb.raw(small_board)
        expected = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        assert small_board == expected


def test_large_board():
    large_board = return_valid_too_large_board()
    vb = create_fake_vestaboard()
    expected_warning = f"The Vestaboard API accepts only 6 lines of characters; you've passed in {len(large_board)}. Only the first 6 will be shown."

    with pytest.warns(UserWarning, match=expected_warning):
        vb.raw(large_board)
        expected = [
            [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
        ]
        assert large_board == expected


def test_multi_screens():
    # fmt: off
    multiScreens = [[[12, 5, 20, 0, 21, 19, 0, 7, 15, 0, 6, 15, 18, 20, 8, 55, 0, 20, 8, 5, 0, 0], [20, 5, 12, 12, 5, 18, 19, 0, 15, 6, 0, 20, 1, 12, 5, 19, 55, 0, 1, 14, 4, 0], [19, 5, 9, 26, 5, 0, 23, 8, 1, 20, 5, 22, 5, 18, 0, 16, 18, 5, 25, 0, 0, 0], [20, 8, 5, 0, 8, 5, 1, 18, 20, 0, 12, 15, 14, 7, 0, 6, 15, 18, 55, 0, 0, 0], [1, 14, 4, 0, 8, 1, 22, 5, 0, 14, 15, 0, 6, 5, 1, 18, 56, 0, 44, 0, 0, 0], [23, 56, 2, 56, 0, 25, 5, 1, 20, 19, 55, 0, 9, 14, 0, 8, 9, 19, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 9, 14, 5, 19, 20, 0, 8, 15, 21, 18, 0, 15, 6, 0, 0, 0, 0, 0, 0, 0, 0], [12, 21, 3, 9, 4, 9, 20, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]]
    # fmt: on
    vb = create_fake_vestaboard()
    vb.sendScreens(multiScreens, 1)


def create_fake_vestaboard():
    i = vestaboard.Installable(
        apiKey=TEST_API_KEY,
        apiSecret=TEST_API_SECRET,
        getSubscription=False,
        saveCredentials=False,
    )
    vb = vestaboard.Board(i, subscriptionId=TEST_SUB_ID)
    return vb


def return_valid_too_small_board():
    return [
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
    ]


def return_valid_too_large_board():
    return [
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [1, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0],
    ]
