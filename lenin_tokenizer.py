"""
This module allows to tokenize a string of characters.
"""
class Token(object):
    """
    Token is a word that consists solely of alphabetic characters
    
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


class Tokenizer(object):
    """
    Class tokenizer that can tokenize a string using method tokenize
    or generate.
    """
    
    def generate(self, text):
        """
        Generator.
        Divides a string into Token instances consisting of alphabetic
        symbols

        Args:
            text (str): String to be tokenized.
        
        Yields:
            Token instances.

        Raises:
            ValueError
        """
        if not type(text) is str:
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
        symbols

        Args:
            text (str): String to be tokenized.
        
        Returns:
            List of Token instances.
            
        Raises:
            ValueError    
        """
        if not type(text) is str:
            raise ValueError
        if not text:
            return []
        tokens = []
        # check the first symbol of a sequence to set initial value of pos
        # pos>=0 is the start position of a word
        # pos=-1 means we are between the words waiting for a new word to start
        if text[0].isalpha():
            pos = 0
        else:
            pos = -1
            
        for i, c in enumerate(text):
            # when the word ends add it to the list, set pos to -1
            if not c.isalpha() and pos>=0:
                tokens.append(Token(pos, text[pos:i]))
                pos = -1
            # finds the beginning of the next word
            if  not text[i-1].isalpha() and c.isalpha():
                pos=i
        # if the last character was alphabetic, we did not add
        # the last token to the list
        if c.isalpha():
            tokens.append(Token(pos, text[pos:i+1]))
        return tokens

def main():
    text = ''
    tok = Tokenizer()
    tokens = tok.tokenize(text)
    for token in tokens:
        print(token.s, token.pos)


if __name__ == "__main__":
    main()
    
