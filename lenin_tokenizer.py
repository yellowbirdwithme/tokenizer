"""
This module allows to tokenize a string of characters.
"""
from unicodedata import category
import shelve
import os


class Token(object):
    """
    Token is a word that consists solely of alphabetic characters.
    
    Attributes:
       pos (int): position of the first character of the token.
       s (str): string represention of the token.
       
    """
    def __init__(self, pos, s):
        """
        Initialises itself.

        Args:
            pos (int): position of the first character of the token.
            s (str): string represention of the token.
        """
        self.pos = pos
        self.s = s
        
    def __repr__(self):
        return self.s + " " + str(self.pos)


class TypeToken(Token):
    """
    TypeToken is Token with a type.
    
    Attributes:
        pos (int): position of the first character of the token.
        s (str): string represention of the token.
        tp (str): type of token. Takes one of following values:
            a - alphabetic
            d - digit
            s - space
            p - punctuation
            o - other
    """
    def __init__(self, pos, s, tp):
        """
        Initialises itself.

        Args:
            pos (int): position of the first character of the token.
            s (str): string represention of the token.
            tp (str): type of token.
        """
        self.pos = pos
        self.s = s
        self.tp = tp


class Tokenizer(object):
    """
    Class tokenizer that can tokenize a string using method tokenize
    or generate.
    """
    def _getType(self, c):
        """
        Gets type of a character.

        Args:
            c (str): character to identify the type of.

        Returns:
            type of the character as string:
                a - alphabetic
                d - digit
                s - space
                p - punctuation
                o - other
        """
        cat = category(c)
        if cat[0] == "L":
            return "a"
        elif cat[0] == "N":
            return "d"
        elif cat[0] == "Z":
            return "s"
        elif cat[0] == "P":
            return "p"
        else:
            return "o"
        
    def generate(self, text):
        """
        Generator.
        Divides a string into Token instances consisting of alphabetic
        symbols.

        Args:
            text (str): String to be tokenized.
        
        Yields:
            Token instances.

        Raises:
            ValueError: in case text is not str.
        """
        if not isinstance(text, str):
            raise ValueError
        
        # check the first symbol of a sequence to set initial value of pos
        # pos>=0 is the start position of a word
        # pos=-1 means we are between the words waiting for a new word to start
        if not text:
            return
        if text[0].isalpha():
            pos = 0
        else:
            pos = -1
        
        for i, c in enumerate(text):
            # when the word ends add it to the list, set pos to -1
            if not c.isalpha() and pos>=0:
                yield Token(pos, text[pos:i])
                pos = -1
            # finds the beginning of the next word
            if  not text[i-1].isalpha() and c.isalpha():
                pos=i
        # if the last character was alphabetic, we did not add
        # the last token to the list
        if c.isalpha():
            yield Token(pos, text[pos:i+1])

    def tokenize(self, text):
        """
        Divides a string into Token instances consisting of alphabetic
        symbols.

        Args:
            text (str): String to be tokenized.
        
        Returns:
            List of Token instances.
            
        Raises:
            ValueError: in case text is not str.
        """
        return list(self.generate(text))

    def generate_with_type(self, text):
        """
        Generator.
        Divides a string into TypeToken instances.
        
        Args:
            text (str): String to be tokenized.
        
        Yields:
            TypeToken instances.

        Raises:
            ValueError: in case text is not str.
        """
        if not isinstance(text, str):
            raise ValueError
        
        if not text:
            return
        
        previousType = ""
        pos = 0
        for i, c in enumerate(text):
            currentType = self._getType(c)
            if currentType != previousType and i>0:
                yield TypeToken(pos, text[pos:i], previousType)
                pos = i
            previousType = currentType
        yield TypeToken(pos, text[pos:i+1], previousType)

    def tokenize_with_type(self, text):
        """
        Divides a string into TypeToken instances.
        
        Args:
            text (str): String to be tokenized.
        
        Returns:
            list of TypeToken instances.

        Raises:
            ValueError: in case text is not str.
        """
        return list(self.generate_with_type(text))
    
    def generate_words_and_numbers(self,text):
        """
        Generator.
        Divides a string into TypeToken instances. Returns only those with type
        'a' or 'd'.
        
        Args:
            text (str): String to be tokenized.
        
        Yields:
            TypeToken instances with type 'a' or 'd' (alpabetic or digit).

        Raises:
            ValueError: in case text is not str.
        """
        for token in self.generate_with_type(text):
            if token.tp == 'a' or token.tp == 'd':
                yield token


def main():
    tokenizer = Tokenizer()
    print(tokenizer.tokenize_with_type("This is my sting!!!111"))


if __name__ == "__main__":
    main()
