import pytest
from vestaboard.formatter import Formatter

validCharacters = [
    [63, 64, 65, 66, 67, 68, 69, 63, 64, 65, 66, 67, 68, 69, 63, 64, 65, 66, 67, 68, 69, 63],
    [64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64],
    [65, 0, 0, 0, 8, 1, 16, 16, 25, 0, 2, 9, 18, 20, 8, 4, 1, 25, 0, 0, 0, 65],
    [66, 0, 0, 0, 0, 0, 0, 0, 13, 9, 14, 1, 20, 15, 37, 0, 0, 0, 0, 0, 0, 66],
    [67, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 67],
    [68, 69, 63, 64, 65, 66, 67, 68, 69, 63, 64, 65, 66, 67, 68, 69, 63, 64, 65, 66, 67, 68]
]

validCharactersResult= {
    'characters': validCharacters
}

def test_standard_formatting():
    assert Formatter()._standard('Love is all you need') == {'text': 'Love is all you need'}, 'Should return a dict with a "text" key and the passed in value.'

def test_raw_formatting():
    assert Formatter()._raw(validCharacters) == validCharactersResult, 'Should return a dict with a "characters" key and the passed in list of lists as the value.'

def test_character_conversion_by_letter():
    assert Formatter().convert('test') == [20, 5, 19, 20], 'Should convert by letter into a list.'

def test_character_conversion_with_invalid_characters_fails():
    with pytest.raises(Exception):
        Formatter().convert('^*^')

def test_character_ignores_case():
    Formatter().convert('tHiS Is A sCHEdulEd TESt')

def test_character_conversion_by_word():
    assert Formatter().convert('test message', byWord=True) == [[20, 5, 19, 20], [13, 5, 19, 19, 1, 7, 5]], 'Should return a list with nested lists - each nested list should contain the character codes.'

def test_word_conversion_with_invalid_characters_fails():
    with pytest.raises(Exception):
        Formatter().convert('test message^*', byWord=True)

def test_convert_line_fails_if_too_many_characters():
    with pytest.raises(Exception):
        Formatter().convertLine('This is too many characters for a line')

def test_convert_line_with_centering():
    assert len(Formatter().convertLine('test message')) == 22, 'Should return a list with 22 elements'
    assert Formatter().convertLine('test message') == [0, 0, 0, 0, 0, 20, 5, 19, 20, 0, 13, 5, 19, 19, 1, 7, 5, 0, 0, 0, 0, 0], 'Should add padding to reach 22 characters'

def test_convert_line_left_justified():
    assert len(Formatter().convertLine('Oh hi!', justify='left')) == 22, 'Should return a list with 22 elements'
    assert Formatter().convertLine('Oh hi!', justify='left') == [15, 8, 0, 8, 9, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Should left justify up to 22 characters'

def test_convert_line_right_justified():
    assert len(Formatter().convertLine('Oh hi!', justify='right')) == 22, 'Should return a list with 22 elements'
    assert Formatter().convertLine('Oh hi!', justify='right') == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 8, 0, 8, 9, 37], 'Should left justify up to 22 characters'

def test_valid_characters_should_pass():
    assert Formatter()._isValid('abcdefghijklmnopqrstuvwxyz1234567890 !@#$()-+&=;:"%,./?°') == True

def test_with_character_code_at_beginning_of_string():
    result = Formatter().convertLine('{23}{1} Test')
    expected = [0, 0, 0, 0, 0, 0, 0, 0, 23, 1, 0, 20, 5, 19, 20, 0, 0, 0, 0, 0, 0, 0]
    assert result == expected

def test_with_character_code_at_end_of_string():
    result = Formatter().convertLine('Test {23}{1}')
    expected = [0, 0, 0, 0, 0, 0, 0, 0, 20, 5, 19, 20, 0, 23, 1, 0, 0, 0, 0, 0, 0, 0]
    assert result == expected

def test_with_character_code_in_middle_of_text():
    result = Formatter().convertLine('Test {23}{1} Test')
    expected = [0, 0, 0, 0, 0, 20, 5, 19, 20, 0, 23, 1, 0, 20, 5, 19, 20, 0, 0, 0, 0, 0]
    assert result == expected

def test_with_text_between_character_codes():
    result = Formatter().convertLine('{48}{3} Test {23}{1}')
    expected = [0, 0, 0, 0, 0, 0, 48, 3, 0, 20, 5, 19, 20, 0, 23, 1, 0, 0, 0, 0, 0, 0]
    assert result == expected

def test_invalid_characters_should_fail():
    assert Formatter()._isValid('^*') == False
    assert Formatter()._isValid('{100}') == False
    assert Formatter()._isValid('{sldkfn}') == False
    assert Formatter()._isValid('{}') == False

def test_regex_finds_valid_character_codes():
    actual = Formatter()._getEmbeddedCharCodes('{24}{1}')
    expected = ['{24}', '{1}']
    assert actual == expected

def test_regex_returns_num_of_extra_characters():
    t1 = Formatter()._numCharacterCodes('{13}{2}')
    e1 = 5
    t2 = Formatter()._numCharacterCodes('{23}{25}{25}')
    e2 = 9
    t3 = Formatter()._numCharacterCodes('There are no codes')
    e3 = 0
    assert t1 == e1
    assert t2 == e2
    assert t3 == e3

def test_formatter_accepts_padding_colors():
    t1 = Formatter().convertLine('red', color='red')
    e1 = [63, 63, 63, 63, 63, 63, 63, 63, 63, 18, 5, 4, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63]
    t2 = Formatter().convertLine('orange', color='orange')
    e2 = [64, 64, 64, 64, 64, 64, 64, 64, 15, 18, 1, 14, 7, 5, 64, 64, 64, 64, 64, 64, 64, 64]
    t3 = Formatter().convertLine('yellow', color='yellow')
    e3 = [65, 65, 65, 65, 65, 65, 65, 65, 25, 5, 12, 12, 15, 23, 65, 65, 65, 65, 65, 65, 65, 65]

    assert t1 == e1
    assert t2 == e2
    assert t3 == e3

def test_formatter_fails_invalid_colors():
    with pytest.raises(KeyError):
        Formatter().convertLine('error', color='pink')

def test_space_buffer_adds_spaces_where_appropriate():
    t1 = Formatter().convertLine('center', justify='center', spaceBuffer=True, color='white')
    t2 = Formatter().convertLine('left', justify='left', spaceBuffer=True, color='white')
    t3 = Formatter().convertLine('right', justify='right', spaceBuffer=True, color='white')
    e1 = [69, 69, 69, 69, 69, 69, 69, 0, 3, 5, 14, 20, 5, 18, 0, 69, 69, 69, 69, 69, 69, 69]
    e2 = [12, 5, 6, 20, 0, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69]
    e3 = [69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 0, 18, 9, 7, 8, 20]

    assert t1 == e1, 'Should add spacing on both sides of centered text'
    assert t2 == e2, 'Should add spacing to the right side of left-justified text'
    assert t3 == e3, 'Should add spacing to the left side of right-justified text'
