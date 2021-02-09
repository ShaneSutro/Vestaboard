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
    assert Formatter._standard('Love is all you need') == {'text': 'Love is all you need'}, 'Should return a dict with a "text" key and the passed in value.'

def test_raw_formatting():
    assert Formatter._raw(validCharacters) == validCharactersResult, 'Should return a dict with a "characters" key and the passed in list of lists as the value.'

def test_character_conversion_by_letter():
    assert Formatter.convert('test') == [20, 5, 19, 20], 'Should convert by letter into a list.'

def test_character_ignores_case():
    Formatter.convert('tHiS Is A sCHEdulEd TESt')

def test_character_conversion_by_word():
    assert Formatter.convert('test message', byWord=True) == [[20, 5, 19, 20], [13, 5, 19, 19, 1, 7, 5]], 'Should return a list with nested lists - each nested list should contain the character codes.'

def test_convert_line_with_centering():
    assert len(Formatter.convertLine('test message')) == 22, 'Should return a list with 22 elements'
    assert Formatter.convertLine('test message') == [0, 0, 0, 0, 0, 20, 5, 19, 20, 0, 13, 5, 19, 19, 1, 7, 5, 0, 0, 0, 0, 0], 'Should add padding to reach 22 characters'

def test_convert_line_left_justified():
    assert len(Formatter.convertLine('Oh hi!', left=True)) == 22, 'Should return a list with 22 elements'
    assert Formatter.convertLine('Oh hi!', left=True) == [15, 8, 0, 8, 9, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Should left justify up to 22 characters'
    
def test_convert_line_right_justified():
    assert len(Formatter.convertLine('Oh hi!', right=True)) == 22, 'Should return a list with 22 elements'
    assert Formatter.convertLine('Oh hi!', right=True) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 8, 0, 8, 9, 37], 'Should left justify up to 22 characters'
