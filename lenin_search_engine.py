"""
This module allows to search in a database and create context windows for further
rpresentation of search results.
"""
import os
import shelve
from lenin_tokenizer import Tokenizer
from lenin_indexer import Position


class Context(object):
    """
    Class Context stores information about the context window of one or
    several words

    Attributes:
        positions (list): list of positions of words for which the context 
                          window was created
        line (str): text of the line that contains the word
        start (int): position of the first character of the context window
        end (int): position after the last character of the context window
    """
    def __init__(self, positions, line, start, end):
        """
        Creates an instance of class Context given the values of its attributes.

        Args:
            positions (list): list of positions of words for which the context 
                              window was created
            line (str): text of the line that contains the word
            start (int): position of the first character of the context window
            end (int): position after the last character of the context window
        """
        self.positions = positions
        self.line = line
        self.start = start
        self.end = end

    @classmethod
    def from_file(cls, filename, position, context_size):
        """
        Creates an instance of class Context from file.

        Args:
            filename (str): path to the file that contains the word.
            position (Position): position of the word to find context for.
            context_size (int): size of the context, number of words to the
                                left and to the right of the word to include
                                to the context window
        Raises:
            ValueError: in case any of the arguments is of the wrong type.
        """
        tok = Tokenizer()
        if not (isinstance(filename, str)
                and isinstance(position, Position)
                and isinstance(context_size, int)):
            raise ValueError

        with open(filename) as f:
            for i, line in enumerate(f):
                if i == position.line:
                    break
        if i != position.line:
            raise ValueError('Wrong line number')
        line = line.strip("\n")
        positions = [position]        
        right_context = line[position.start:]
        left_context = line[:position.end][::-1]
        
        for i, token in enumerate(tok.generate_AD(left_context)):
            if i == context_size:
                break
        start = position.end - token.pos - len(token.s)
        for i, token in enumerate(tok.generate_AD(right_context)):
            if i == context_size:
                break
        end = position.start + token.pos + len(token.s)
        return cls(positions, line, start, end)

    def isintersected(self, obj):
        """
        This method checks if two context windows intersect.
        """
        return (self.start <= obj.end and
                self.end >= obj.start and
                obj.line == self.line)

    def join(self, obj):
        """
        This method joins two context windows by changing self.
        """
        for position in obj.positions:
            if position not in self.positions:
                self.positions.append(position)
        self.start = min(self.start, obj.start)
        self.end = max(self.end, obj.end)
        
    def __eq__(self, obj):
        """
        Check if two context windows are equal.
        """
        return ((self.positions == obj.positions) and
                (self.line == obj.line) and
                (self.start == obj.start) and
                (self.end == obj.end))

    def __repr__(self):
        return str(self.positions)+ ', ' + str(self.start)+ ', ' \
               + str(self.end)+ ', ' + self.line
            

        
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
        query = list(self.tok.generate_AD(query))
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

    def get_context_windows(self, search_results, context_size):
        """
        This method creates a dictionary of files and contexts given a dictionary
        of files and positions.

        Args:
            search_results (dict): a dictionary of files and positions.
            context_size (int): size of context, number of words to the left and
                                to the right of the word to include to the context
                                window
        Returns:
            Dictionary of files and contexts in format {filename: [contexts]}

        """
        if not (isinstance(search_results, dict) and
                isinstance(context_size, int)):
            raise ValueError
        
        contexts_dict = {}
        null = Context([], "", 0, 0)
        for f, positions in search_results.items():
            previous_context = null
            for position in positions:
                current_context = Context.from_file(f, position, context_size)
                if previous_context.isintersected(current_context):
                    previous_context.join(current_context)
                else:
                    if previous_context is not null:
                        contexts_dict.setdefault(f, []).append(previous_context)
                    previous_context = current_context
            contexts_dict.setdefault(f, []).append(previous_context)

        return contexts_dict
                
    def __del__(self):
        self.db.close()


def main():
    se = SearchEngine("tolstoy_db")
    print(se.multiword_search(input()))
    del se


if __name__ == '__main__':
    main()
