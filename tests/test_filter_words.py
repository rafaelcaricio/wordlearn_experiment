from wordlearn import filter_words


def test_filter_a_simple_sentence():
    assert filter_words('this is a sentence') == ['sentence']

def test_filter_with_numbers():
    words = filter_words('the player number 1 is now the winner')
    assert len(words) == 3
    assert words == ['player', 'number', 'winner']

def test_filter_words_with_comma():
    words = filter_words('the player: 1 is now the winner.')
    assert words == ['player', 'winner']

def test_filter_words_with_dash():
    words = filter_words('the player: 1 is now the JSON-like.')
    assert words == ['player', 'json-like']

def test_filter_words_with_apostrophes():
    words = filter_words('Jason`s and Sue\'s children!!!')
    assert words == ['jason`s', 'sue\'s', 'children']

def test_some_random_sentence():
    words = filter_words('Introduces ambiguity (unless the context happens to resolve it): read in.')
    assert words == ['introduces', 'ambiguity', 'unless', 'context', 'happens', 'resolve', 'read']
