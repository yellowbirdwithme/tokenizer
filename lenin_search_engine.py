import os
import shelve
from lenin_tokenizer import Tokenizer


class SearchEngine(object):
    """
    Search Engine to perform search against a database. Each instance of
    class SearchEngine works with its own database that is specfied during
    initialisation.

    Attributes:
        db (shelf): database to search against.
    """
    def __init__(self, path):
        """
        Initialize itself.

        Args:
            path (str): path to database
        """
        self.db = shelve.open(path)
        self.tok = Tokenizer()
        
    def simple_search(self, query):
        """
        Performs simple search against the database. Returns a dictionary of
        files and positions for the given word in query.
        
        Args:
            query (str): search query
        """
        if not isinstance(query, str):
            raise ValueError

        return self.db.get(query, {})
        
    def __del__(self):
        self.db.close()


def main():
    se = SearchEngine("test")


if __name__ == "__main__":
    main()
