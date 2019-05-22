"""
This module allows to search in a database and create context windows for further
rpresentation of search results.
"""
import os
import re
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
            raise ValueError (filename, position, context_size)

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

    def to_sentence(self):
        """
        This method expands the boundaries of the context window up to the
        sentence boundaries.
        """
        boundary_r = re.compile(r'[.!?] [A-ZА-Я]')
        boundary_l = re.compile(r'[A-ZА-Я] [.!?]')
        right = self.line[self.end:]
        left = self.line[:self.start+1][::-1]        
        if left:
            try:
                self.start = self.start - boundary_l.search(left).start()
            except:
                self.start = 0
        if right:
            try:
                self.end += boundary_r.search(right).start() + 1
            except:
                self.end = len(self.line)

    def cut_and_highlight(self):
        """
        Creates a string that represents context. Query words are 'highlighted'
        i.e. surrounded by HTML tags <b></b>.

        Returns:
            String cut to size of the context with query words highlighted.
        """
        quote = self.line[self.start:self.end]
        cl = '</b>'
        op = '<b>'
        for position in reversed(self.positions):
            end = position.end - self.start
            start = position.start - self.start
            quote = quote[:end] + cl + quote[end:]
            quote = quote[:start] + op + quote[start:]
        return quote
        
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
        
        files_found = simple_search_results[0]
        for result in simple_search_results:
            files_found.intersection_update(result)
        final_result = {}
        for f in files_found:
            for word in query:
                final_result.setdefault(f, []).extend(self.db[word.s][f])
            final_result[f].sort()
        return final_result

    def get_context_windows(self,
                            input_dict,
                            context_size=3):
        """
        This method creates a dictionary of files and contexts given a
        dictionary of files and positions.

        Args:
            search_results (dict): a dictionary of files and positions.
            context_size (int): size of context, number of words to the left and
                                to the right of the word to include to the context
                                window
            
        Returns:
            Dictionary of files and contexts in format {filename: [contexts]}

        """
        if not (isinstance(input_dict, dict) and
                isinstance(context_size, int)):
            raise ValueError
        
        contexts_dict = {}
        
        for f, positions in input_dict.items():
            for position in positions:
                context = Context.from_file(f, position, context_size)
                contexts_dict.setdefault(f, []).append(context)

        joined_contexts_dict = self.join_contexts(contexts_dict)

        return joined_contexts_dict

    def join_contexts(self, input_dict):
        """
        This method joins intersecting windows in a dictionary of files and
        context windows.

        Args:
            input_dict (dict): a dictionary of files and context windows of the
                               following structure {file: [contexts]}
        Returns a dictionary of files and joined contexts {file: [contexts]}
        """
        contexts_dict = {}
        null = Context([], "", 0, 0)
        for f, contexts in input_dict.items():
            previous_context = null
            for context in contexts:
                if previous_context.isintersected(context):
                    previous_context.join(context)
                else:
                    if previous_context is not null:
                        contexts_dict.setdefault(f, []).append(previous_context)
                    previous_context = context
            contexts_dict.setdefault(f, []).append(previous_context)

        return contexts_dict

    def search_to_context(self, query, context_size=3):
        """
        Performs a search of a multiword query against the database. Returns
        a dictionary of files, that contain all the words of the query. If any
        of the words of the query is not in the database, no files will be
        found.
        The values in the dictionary are contexts of the found words joined
        if intersecting each other.

        Args:
            query (str): search query
            context_size (int): size of the context window

        Returns:
            Dictionary of files and contexts of all the words of the query
            in a given file in the format {filename: [contexts]}
        """
        positions_dict = self.multiword_search(query)
        context_dict = self.get_context_windows(positions_dict, context_size)
        return context_dict

    def search_to_sentence(self, query, context_size=3):
        """
        Performs a search of a multiword query against the database. Returns
        a dictionary of files, that contain all the words of the query. If any
        of the words of the query is not in the database, no files will be
        found.
        The values in the dictionary are contexts of the found words extended to
        the sentence boundaries and joined if intersecting each other.

        Args:
            query (str): search query
            context_size (int): size of the initial context window built for
                                search results

        Returns:
            Dictionary of files and contexts of all the words of the query
            in a given file in the format {filename: [contexts]}
        """
        context_dict = self.search_to_context(query, context_size)
        for contexts in context_dict.values():
            for context in contexts:
                context.to_sentence()
        sentence_dict = self.join_contexts(context_dict)
        return sentence_dict

    def search_to_quote(self, query, context_size=3):
        """
        Performs a search of a multiword query against the database. Returns
        a dictionary of files, that contain all the words of the query. If any
        of the words of the query is not in the database, no files will be
        found.
        The values in the dictionary are quotes with found words surrounded by
        <b></b> HTML tags.

        Args:
            query (str): search query
            context_size (int): size of the initial context window built for
                                search results

        Returns:
            Dictionary of files and quotes of all the words of the query
            in a given file in the format {filename: [quotes(str)]}
        """
        sentence_dict = self.search_to_sentence(query, context_size)
        quote_dict = {}
        for f, contexts in sentence_dict.items():
            for context in contexts:
                quote_dict.setdefault(f, []).append(context.cut_and_highlight())
        return quote_dict
        
                
    def __del__(self):
        self.db.close()


def main():
    se = SearchEngine("tolstoy_db")
    print(se.multiword_search(input()))
    del se


if __name__ == '__main__':
    main()
