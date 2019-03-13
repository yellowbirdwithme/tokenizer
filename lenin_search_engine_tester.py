import unittest
import os
import shelve
from lenin_search_engine import SearchEngine
from lenin_indexer import Position


# The test files are following:
# test.txt: "this is a test text\nit is to test search engine"
# test1.txt: "another text to test the search engine"
# test2.txt: "cat\ndog\nmouse\nelephant\nchicken\nthese are animals"

DB = {'this': {'test.txt': [Position(0, 0, 4)]},
      'is': {'test.txt': [Position(0, 5, 7),
                          Position(1, 3, 5)]},
      'a': {'test.txt': [Position(0, 8, 9)]},
      'test': {'test.txt': [Position(0, 10, 14),
                            Position(1, 9, 13)],
               'test1.txt': [Position(0, 16, 20)]},
      'text': {'test.txt': [Position(0, 15, 19)],
               'test1.txt': [Position(0, 8, 12)]},
      'it': {'test.txt': [Position(1, 0, 2)]},
      'to': {'test.txt': [Position(1, 6, 8)],
             'test1.txt': [Position(0, 13, 15)]},
      'search': {'test.txt': [Position(1, 14, 20)],
                 'test1.txt': [Position(0, 25, 31)]},
      'engine': {'test.txt': [Position(1, 21, 27)],
                 'test1.txt': [Position(0, 32, 38)]},
      'another': {'test1.txt': [Position(0, 0, 7)]},
      'the': {'test1.txt': [Position(0, 21, 24)]},
      'cat': {'test2.txt': [Position(0, 0, 3)]},
      'dog': {'test2.txt': [Position(1, 0, 3)]},
      'mouse': {'test2.txt': [Position(2, 0, 5)]},
      'elephant': {'test2.txt': [Position(3, 0, 8)]},
      'chicken': {'test2.txt': [Position(4, 0, 7)]},
      'these': {'test2.txt': [Position(5, 0, 5)]},
      'are': {'test2.txt': [Position(5, 6, 9)]},
      'animals': {'test2.txt': [Position(5, 10, 17)]}}


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
        self.assertEqual(result, {"test.txt": [Position(0, 10, 14),
                                               Position(1, 9, 13)],
                                  "test1.txt": [Position(0, 16, 20)]})
        
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
        self.assertEqual(result, {'test.txt': [Position(0, 10, 14),
                                               Position(1, 6, 8),
                                               Position(1, 9, 13)],
                                  'test1.txt': [Position(0, 13, 15),
                                                Position(0, 16, 20)]})
        
    def test_far_words(self):
        result = self.se.multiword_search("cat animals")
        self.assertEqual(result, {'test2.txt': [Position(0, 0, 3),
                                                Position(5, 10, 17)]})

    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)

                
if __name__ == '__main__':
    unittest.main()
