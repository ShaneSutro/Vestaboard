import vestaboard.formatter as formatter

def test_standard_formatting():
    assert formatter.standard('Love is all you need') == {'text': 'Love is all you need'}, 'Should return a dict with a "text" key and the passed in value.'