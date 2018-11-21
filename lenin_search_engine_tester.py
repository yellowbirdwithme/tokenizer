import unittest
import os
import shelve
from lenin_search_engine import SearchEngine
from lenin_indexer import Indexer, Position


class SimpleSearchTest(unittest.TestCase):
    """
    Tests method simple_search of class SearchEngine
    """
    def setUp(self):
        self.ind = Indexer("test_db")
        with open("test.txt", "wt") as f:
            f.write("this is a test text\nit is to test search engine")
        with open("test1.txt", 'wt') as f:
            f.write("another text to test the search engine")
        self.ind.index("test.txt")
        self.ind.index("test1.txt")
        del self.ind
        self.se = SearchEngine("test_db")

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
        os.remove('test1.txt')
        os.remove('test.txt')

    
if __name__ == '__main__':
    unittest.main()
