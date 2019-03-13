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

        Returns:
            Dictionary of files and positions in format {filename: [positions]}

        Raises:
            ValueError: in case query is not str.
        """
        if not isinstance(query, str):
            raise ValueError

        return self.db.get(query, {})

    def multiword_search(self, query):
        """
        Performs a search of a multiword query against the database. Returns
        a dictionary of files, that contain all the words of the query. If any
        of the words of the query is not in the database, no files will be
        found.

        Args:
            query (str): search query

        Returns:
            Dictionary of files and positions of all the words of the query
            in a given file in the format {filename: [positions of all words]}

        Raises:
            ValueError: in case query is not str.
        """
        if not isinstance(query, str):
            raise ValueError
        
        tokenizer = Tokenizer()
        query = list(tokenizer.generate_words_and_numbers(query))
        simple_search_results = []
        for word in query:
            simple_search_results.append(set(self.simple_search(word.s)))

        if not simple_search_results:
            return {}
        
        files_found = simple_search_results[1]
        for result in simple_search_results:
            files_found.intersection_update(result)
        final_result = {}
        for f in files_found:
            for word in query:
                final_result.setdefault(f, []).extend(self.db[word.s][f])
            final_result[f].sort()
        return final_result
        
    def __del__(self):
        self.db.close()


def main():
    se = SearchEngine("tolstoy_db")
    print(se.multiword_search(input()))
    del se


if __name__ == '__main__':
    main()
