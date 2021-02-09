from vestaboard.characters import characters

class Formatter:
  def _standard(text):
    return {'text': text}

  def _raw(charList):
    return {'characters': charList}

  def convert(inputString, byLetter=True, byWord=False):
    inputString = inputString.lower()
    converted = []
    if byWord:
      wordList = inputString.split(' ')
      for word in wordList:
        convertedWord = []
        for letter in word:
          convertedWord.append(characters[letter])
        converted.append(convertedWord)
    elif byLetter:
      for letter in inputString:
        converted.append(characters[letter])

    return converted

  def convertLine(inputString, center=True, left=False, right=False):
    inputString = inputString.lower()
    converted = []
    if len(inputString) > 22:
      return Exception('Convert line method takes in a string less than or equal to 22 characters.')
    if left:
      inputString = inputString.ljust(22)
    elif right:
      inputString = inputString.rjust(22)
    elif center:
      inputString = inputString.center(22)
    for letter in inputString:
      converted.append(characters[letter])

    return converted    