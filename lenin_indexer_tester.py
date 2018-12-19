import unittest
import os
import shelve
from collections import Generator
from lenin_indexer import Indexer, Position


class IndexerTest(unittest.TestCase):
    """
    Tests method index of class Indexer
    """
    def setUp(self):
        self.indexer = Indexer("test_db")
            
    def test_error_wrong_input_number(self):
        with self.assertRaises(ValueError):
            self.indexer.index(42)
            
    def test_error_wrong_input_list(self):
        with self.assertRaises(ValueError):
            self.indexer.index(["test.txt"])

    def test_error_wrong_input_wrong_path(self):
        with self.assertRaises(FileNotFoundError): 
            self.indexer.index("file.txt")

    def test_empty_file(self):
        with open("test.txt", 'tw') as f:
            f.write("")
        self.indexer.index("test.txt")
        self.assertEqual(dict(self.indexer.db), {})
            
    def test_one_word(self):
        with open("test.txt", 'tw') as f:
            f.write("test")
        self.indexer.index("test.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'test': {'test.txt': [Position(0, 0, 4)]}})
        
    def test_two_identical_words(self):
        with open("test.txt", 'tw') as f:
            f.write("test test")
        self.indexer.index("test.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'test': {'test.txt': [Position(0, 0, 4),
                                                Position(0, 5, 9)]}})
        
    def test_two_different_words(self):
        with open("test.txt", 'tw') as f:
            f.write("test case")
        self.indexer.index("test.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'test': {'test.txt': [Position(0, 0, 4)]},
                          'case': {'test.txt': [Position(0, 5, 9)]}})

    def test_two_files(self):
        with open("test.txt", 'tw') as f:
            f.write("file one")
        with open("test1.txt", 'tw') as f:
            f.write("file two")
        self.indexer.index("test.txt")
        self.indexer.index("test1.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'file': {'test.txt': [Position(0, 0, 4)],
                                  'test1.txt': [Position(0, 0, 4)]},
                          'one': {'test.txt': [Position(0, 5, 8)]},
                          'two': {'test1.txt': [Position(0, 5, 8)]}})

    def test_multiple_lines(self):
        with open("test.txt", 'tw') as f:
            f.write("""test\nme\nplease""")
        self.indexer.index("test.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'test': {'test.txt': [Position(0, 0, 4)]},
                          'me': {'test.txt': [Position(1, 0, 2)]},
                          'please': {'test.txt': [Position(2, 0, 6)]}})
        
    def tearDown(self):
        del self.indexer
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)
        if 'test1.txt' in os.listdir('.'):
            os.remove('test1.txt')
        if 'test.txt' in os.listdir('.'):
            os.remove('test.txt')
        

if __name__ == '__main__':
    unittest.main()
