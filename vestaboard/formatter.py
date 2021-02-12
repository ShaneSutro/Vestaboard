from vestaboard.characters import characters
from vestaboard.characters import colors
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
    test = "^(?:[A-Za-z0-9!@#$\(\)\-+&=;:'\"%,./?°\s ]*(?:\{[0-9]+\})*[A-Za-z0-9!@#$\(\)\-+&=;:'\"%,./?°\s ]*)*$"

    return bool(re.match(test, inputString))

  @staticmethod
  def _getEmbeddedCharCodes(inputString):
    test = "\{[0-9]+\}+"

    return re.findall(test, inputString)

  def _numCharacterCodes(self, inputString):
    embeddedCharacterCodes = self._getEmbeddedCharCodes(inputString)
    numCharacterCodes = 0
    for match in embeddedCharacterCodes:
      numCharacterCodes += 2 + (len(match) - 3)

    return numCharacterCodes

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

  def convertLine(self, inputString, justify='center', color=' ', spaceBuffer=False):
    if not self._isValid(inputString):
      raise Exception('Your text contains one or more characters that the Vestaboard does not support.')
    numCharacterCodes = self._numCharacterCodes(inputString)
    if spaceBuffer:
      inputString = self._addSpaceBuffer(inputString, justify)
    inputString = inputString.lower()
    if color != ' ':
      try:
        color = colors[color]
      except KeyError:
        raise KeyError('Valid colors are red, orange, yellow, green, blue, violet, white, and black (default black).')
    converted = []
    if len(inputString) - numCharacterCodes > 22:
      raise Exception(f'Convert line method takes in a string less than or equal to 22 characters - string passed in was {len(inputString)} characters. Reduce size and try again (remember that setting spaceBuffer=True increases your line size by 2).')
    inputString = self._justifyContent(inputString, justify, numCharacterCodes, color)

    skipTo = 0
    for index, letter in enumerate(inputString):
      if index < skipTo:
        continue
      if letter == '{':
        if inputString[index + 3] == '}': #two-digit character code like {63}
          converted.append(int(inputString[index + 1: index + 3]))
          skipTo = index + 4
        elif inputString[index + 2] == '}': #one-digit character code like {4}
          converted.append(int(inputString[index + 1: index + 2]))
          skipTo = index + 3
      else:
        converted.append(characters[letter])

    return converted

  @staticmethod
  def _addSpaceBuffer(inputString, justify):
    if justify == 'left':
      return inputString + ' '
    elif justify == 'right':
      return ' ' + inputString
    else:
      return ' ' + inputString + ' '

  @staticmethod
  def _justifyContent(inputString, justify, numCharacterCodes, color):
    if justify == 'left':
      inputString = inputString.ljust(22 + numCharacterCodes, '^')
    elif justify == 'right':
      inputString = inputString.rjust(22 + numCharacterCodes, '^')
    elif justify == 'center':
      inputString = inputString.center(22 + numCharacterCodes, '^')
    inputString = inputString.replace('^', color)

    return inputString

