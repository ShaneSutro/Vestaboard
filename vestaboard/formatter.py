import warnings
import textwrap
import re
import math
from vestaboard.characters import characters
from vestaboard.characters import colors
from vestaboard.characters import reverseCharacters


class Formatter:
    def __init__(self):
        self.name = "Formatter"

    def _standard(self, text):
        if not self._isValid(text):
            raise ValueError(
                "Your text contains one or more characters that the Vestaboard does not support."
            )
        return {"text": text}

    @staticmethod
    def _raw(charList):
        return {"characters": charList}

    @staticmethod
    def _isValid(inputString):
        inputString = inputString.lower()
        test = r"^(?:[A-Za-z\d!@#$()\-+&=;:'\"%,./?°\s]|(?:\{\d{1,2}\}))*$"

        return bool(re.match(test, inputString))

    @staticmethod
    def _getEmbeddedCharCodes(inputString):
        test = r"\{[0-9]+\}+"

        return re.findall(test, inputString)

    def _numCharacterCodes(self, inputString):
        embeddedCharacterCodes = self._getEmbeddedCharCodes(inputString)
        numCharacterCodes = 0
        for match in embeddedCharacterCodes:
            numCharacterCodes += 2 + (len(match) - 3)

        return numCharacterCodes

    def convert(self, inputString, byLetter=True, byWord=False):
        if not self._isValid(inputString):
            raise Exception(
                "Your text contains one or more characters that the Vestaboard does not support."
            )
        inputString = inputString.lower()
        converted = []
        if byWord:
            wordList = inputString.split(" ")
            for word in wordList:
                convertedWord = self._convertLoop(word)
                converted.append(convertedWord)
        elif byLetter:
            converted += self._convertLoop(inputString)

        return converted

    def convertLine(self, inputString, justify="center", color=" ", spaceBuffer=False):
        if not self._isValid(inputString):
            raise Exception(
                "Your text contains one or more characters that the Vestaboard does not support."
            )
        numCharacterCodes = self._numCharacterCodes(inputString)
        if spaceBuffer:
            inputString = self._addSpaceBuffer(inputString, justify)
        inputString = inputString.lower()
        if color != " ":
            try:
                color = colors[color]
            except KeyError as exc:
                raise KeyError(
                    "Valid colors are red, orange, yellow, green, blue, violet, white, and black (default black)."
                ) from exc
        converted = []
        if len(inputString) - numCharacterCodes > 22:
            raise Exception(
                f"Convert line method takes in a string less than or equal to 22 characters - string passed in was {len(inputString)} characters. Reduce size and try again (remember that setting spaceBuffer=True increases your line size by 2)."
            )
        inputString = self._justifyContent(
            inputString, justify, numCharacterCodes, color
        )

        converted = self._convertLoop(inputString)

        return converted

    @staticmethod
    def _convertLoop(inputString):
        converted = []
        skipTo = 0
        for index, letter in enumerate(inputString):
            if index < skipTo:
                continue
            if letter == "{":
                if inputString[index + 2] == "}":  # one-digit character code like {4}
                    converted.append(int(inputString[index + 1 : index + 2]))
                    skipTo = index + 3
                elif (
                    inputString[index + 3] == "}"
                ):  # two-digit character code like {63}
                    converted.append(int(inputString[index + 1 : index + 3]))
                    skipTo = index + 4
            else:
                converted.append(characters[letter])

        return converted

    @staticmethod
    def _addSpaceBuffer(inputString, justify):
        if justify == "left":
            return inputString + " "
        elif justify == "right":
            return " " + inputString
        else:
            return " " + inputString + " "

    @staticmethod
    def _justifyContent(inputString, justify, numCharacterCodes, color):
        if justify == "left":
            inputString = inputString.ljust(22 + numCharacterCodes, "^")
        elif justify == "right":
            inputString = inputString.rjust(22 + numCharacterCodes, "^")
        elif justify == "center":
            inputString = inputString.center(22 + numCharacterCodes, "^")
        inputString = inputString.replace("^", color)

        return inputString

    @staticmethod
    def _reverse_convert(charArray, normalize: bool = False):
        convertedArray = []
        for line in charArray:
            newLine = []
            for character in line:
                newLine.append(reverseCharacters[character])
            if normalize:
                convertedArray.append("".join(newLine))
            else:
                convertedArray.append(newLine)
        if normalize:
            return "\n".join(convertedArray)
        else:
            return convertedArray

    def _add_vestaboard_spacing(self, lines, size=None, justify="left"):
        if size is None:
            size = [6, 22]
        _, maxChars = size
        longestLine = 0
        for line in lines:
            lineLength = len(line)
            if lineLength > longestLine:
                longestLine = lineLength

        numSpacesNeeded = 0
        if maxChars > longestLine:
            numSpacesNeeded = math.floor((maxChars - longestLine) / 2)

        paddedLines = []
        for line in lines:
            lineLength = len(line)
            if justify == "left":
                paddedLines.append(
                    self.convertLine(
                        " " * numSpacesNeeded
                        + line
                        + " " * (maxChars - lineLength - numSpacesNeeded)
                    )
                )
            elif justify == "right":
                paddedLines.append(
                    self.convertLine(
                        " " * (maxChars - lineLength - numSpacesNeeded)
                        + line
                        + " " * numSpacesNeeded
                    )
                )

        return paddedLines

    def convertPlainText(
        self,
        text,
        size=None,
        justify="center",
        align="center",
        useVestaboardCentering=False,
    ):
        if size is None:
            size = [6, 22]
        maxRows, maxCols = size
        splitLines = []
        for linebreak in text.split("\n"):
            splitLines += textwrap.fill(linebreak, maxCols).split("\n")
        if len(splitLines) > maxRows:
            warningMessage = f"This text is too long to fit within the space specified ({maxRows} rows of {maxCols} characters each). Only the first {maxRows} rows are being returned."
            warnings.warn(warningMessage)

        convertedLines = []

        if useVestaboardCentering:
            if justify == "center":
                warnings.warn(
                    "Vestaboard formatting only affects left or right-justified text. Because of this, your text will be left justified by default. If you don't want your text left justified, remove `useVestaboardCentering` from your function call."
                )
                convertedLines = self._add_vestaboard_spacing(splitLines, size)
            else:
                convertedLines = self._add_vestaboard_spacing(splitLines, size, justify)
        else:
            for line in splitLines:
                convertedLines.append(self.convertLine(line, justify, "black", False))

        if len(convertedLines) < maxRows:
            blankLine = [0] * maxCols
            while len(convertedLines) < maxRows:
                if align == "bottom":
                    convertedLines.insert(0, blankLine)
                else:
                    convertedLines.append(blankLine)

                if len(convertedLines) < maxRows:
                    if align == "top":
                        convertedLines.append(blankLine)
                    else:
                        convertedLines.insert(0, blankLine)

        return convertedLines[0:maxRows]
