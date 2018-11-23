import unittest
import os
import shelve
from lenin_search_engine import SearchEngine
from lenin_indexer import Position


# The test files are following:
# test.txt: "this is a test text\nit is to test search engine"
# test1.txt: "another text to test the search engine"
# test2.txt: "cat\ndog\nmouse\nelephant\nchicken\nthese are animals"

DB = {'this': {'test.txt': [Position(0, 4, 0)]},
      'is': {'test.txt': [Position(5, 7, 0),
                          Position(3, 5, 1)]},
      'a': {'test.txt': [Position(8, 9, 0)]},
      'test': {'test.txt': [Position(10, 14, 0),
                            Position(9, 13, 1)],
               'test1.txt': [Position(16, 20, 0)]},
      'text': {'test.txt': [Position(15, 19, 0)],
               'test1.txt': [Position(8, 12, 0)]},
      'it': {'test.txt': [Position(0, 2, 1)]},
      'to': {'test.txt': [Position(6, 8, 1)],
             'test1.txt': [Position(13, 15, 0)]},
      'search': {'test.txt': [Position(14, 20, 1)],
                 'test1.txt': [Position(25, 31, 0)]},
      'engine': {'test.txt': [Position(21, 27, 1)],
                 'test1.txt': [Position(32, 38, 0)]},
      'another': {'test1.txt': [Position(0, 7, 0)]},
      'the': {'test1.txt': [Position(21, 24, 0)]},
      'cat': {'test2.txt': [Position(0, 3, 0)]},
      'dog': {'test2.txt': [Position(0, 3, 1)]},
      'mouse': {'test2.txt': [Position(0, 5, 2)]},
      'elephant': {'test2.txt': [Position(0, 8, 3)]},
      'chicken': {'test2.txt': [Position(0, 7, 4)]},
      'these': {'test2.txt': [Position(0, 5, 5)]},
      'are': {'test2.txt': [Position(6, 9, 5)]},
      'animals': {'test2.txt': [Position(10, 17, 5)]}}


class SimpleSearchTest(unittest.TestCase):
    """
    Tests method simple_search of class SearchEngine
    """
    def setUp(self):
        self.se = SearchEngine("test_db")
        self.se.db.update(DB)

    def test_wrong_input_error(self):
        with self.assertRaises(ValueError):
            self.se.simple_search(123)

    def test_empty_input(self):
        result = self.se.simple_search("")
        self.assertEqual(result, {})

    def test_no_alph_or_num_in_input(self):
        result = self.se.simple_search("!!!")
        self.assertEqual(result, {})
        
    def test_absent_key(self):
        result = self.se.simple_search("turtle")
        self.assertEqual(result, {})
        
    def test_actual_key(self):
        result = self.se.simple_search("test")
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"test.txt": [Position(10, 14, 0),
                                               Position(9, 13, 1)],
                                  "test1.txt": [Position(16, 20, 0)]})
        
    def test_two_words_input(self):
        result = self.se.simple_search("test me")
        self.assertEqual(result, {})
        
    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)


class MultiwordSearchTest(unittest.TestCase):
    """
    Tests method multiword_search of SearchEngine.
    """
    def setUp(self):
        self.se = SearchEngine("test_db")
        self.se.db.update(DB)

    def test_wrong_input_error(self):
        with self.assertRaises(ValueError):
            self.se.multiword_search(123)

    def test_empty_input(self):
        result = self.se.multiword_search("")
        self.assertEqual(result, {})

    def test_no_alph_or_num_in_input(self):
        result = self.se.multiword_search("!!!")
        self.assertEqual(result, {})

    def test_absent_key(self):
        result = self.se.multiword_search("turtle test")
        self.assertEqual(result, {})

    def test_adjacent_words(self):
        result = self.se.multiword_search("to test")
        self.assertEqual(result, {'test.txt': [Position(6, 8, 1),
                                               Position(10, 14, 0),
                                               Position(9, 13, 1)],
                                  'test1.txt': [Position(13, 15, 0),
                                                Position(16, 20, 0)]})
        
    def test_far_words(self):
        result = self.se.multiword_search("cat animals")
        self.assertEqual(result, {'test2.txt': [Position(0, 3, 0),
                                                Position(10, 17, 5)]})

    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)

                
if __name__ == '__main__':
    unittest.main()
