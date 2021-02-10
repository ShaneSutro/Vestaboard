from vestaboard.characters import characters
import re

class Formatter:
  def __init__(self):
    self.name = "Formatter"

  def _standard(self, text):
    if not self._isValid(text):
      raise Exception('Your text contains one or more characters that the Vestaboard does not support.')
    return {'text': text}

  @staticmethod
  def _raw(charList):
    return {'characters': charList}

  @staticmethod
  def _isValid(inputString):
    inputString = inputString.lower()
    test = "^[A-Za-z0-9!@#$\(\)\-+&=;:'\"%,./?°\s ]*(?:\{[0-9]+\})*[A-Za-z0-9!@#$\(\)\-+&=;:'\"%,./?°\s ]*$"

    return bool(re.match(test, inputString))

  def convert(self, inputString, byLetter=True, byWord=False):
    if not self._isValid(inputString):
      raise Exception('Your text contains one or more characters that the Vestaboard does not support.')
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

  def convertLine(self, inputString, center=True, left=False, right=False):
    if not self._isValid(inputString):
      raise Exception('Your text contains one or more characters that the Vestaboard does not support.')
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
