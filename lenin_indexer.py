"""
This module allows to index a string of characters.
"""
import shelve
import os
from lenin_tokenizer import Tokenizer


class Position(object):
    """
    Position stores data about the position of the first and the last
    character of a token.

    Attributes:
        start (int): position of the first character of the token.
        end (int): position after the last character of the token.
        line (int): line in which the token is.
    """
    def __init__(self, start, end, line):
        """
        Creates an instance of class Position using start and end positions.

        Args:
            start (int): position of the first character of the token.
            end (int): position after the last character of the token.
            line (int): line in which the token is.
        """
        self.line = line
        self.start = start
        self.end = end
        
    @classmethod
    def from_token(cls, token, line):
        """
        Allows to create an instance of class Position using a token.

        Args:
            token (Token): token to get the position of.
            line (int): line in which the token is.
        """
        return cls(token.pos, token.pos + len(token.s), line)
    
    def __eq__(self, obj):
        """
        Checks if two instances of class Position are equal.
        Two instances of class Positon are equal if their start and end
        attributes are equal.

        Args:
            obj (Position): instance to compare the given token to.
        """
        return (self.start == obj.start and
                self.end == obj.end and
                self.line == obj.line)

    def __repr__(self):
        return '(' + str(self.start) + ',' + str(self.end) + ',' + \
               str(self.line) + ")" 
        
    
class Indexer(object):
    """
    Class Indexer allows to index files and write the indexes of tokens into a
    database. Every instance of class Indexer works with its own database.

    Attributes:
        db (shelf): database this instance of class Indexer works with.
    """
    def __init__(self, path):
        """
        Initialize itself.

        Args:
            path (str): path to database.
        """
        self.db = shelve.open(path, writeback=True)
        
    def index(self, path):
        """
        Method index indexes a file by line and writes indexes into database
        self.db.

        Args:
            path (str): path to the file to be indexed.
        """
        tokenizer = Tokenizer()
        
        if not isinstance(path, str):
            raise ValueError
        
        try:
            file = open(path)       
        except IOError:
            raise FileNotFoundError("File not found or path is incorrect")

        # tokenize text, add tokens to database
        for i, line in enumerate(file):
            for token in tokenizer.generate_words_and_numbers(line):
                self.db.setdefault(token.s, {}).setdefault(path, []).append(
                    Position.from_token(token, i)
                )
        file.close()

    def __del__(self):
        self.db.close()
        

def main():
    for filename in os.listdir('.'):
        if filename.startswith("test_db."):
            os.remove(filename)
    ind = Indexer("test_db")
    with open('test.txt', 'tw') as f:
        f.write('''test me please\ni have\nmany\nlines)))''')
    ind.index("test.txt")
    print(dict(ind.db))
    os.remove('test.txt')
    del ind
    for filename in os.listdir('.'):
        if filename.startswith("test_db."):
            os.remove(filename)


if __name__ == "__main__":
    main()
