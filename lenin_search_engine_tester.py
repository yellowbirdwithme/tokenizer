import unittest
import os
import shelve
from lenin_search_engine import SearchEngine, Context
from lenin_indexer import Position


# The test files are following:
TEST = "this is a test text\nit is to test search engine"
TEST1 = "another text to test the search engine"
TEST2 = "cat\ndog\nmouse\nelephant\nchicken\nthese are animals"
TEST3 = "Я не люблю красные бобы, белые бобы и бобы вообще. Противные бобы. Дурацкие бобы."

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
      'animals': {'test2.txt': [Position(5, 10, 17)]},
      'Я': {'test3.txt': [Position(0, 0, 1)]},
      'не': {'test3.txt': [Position(0, 2, 4)]},
      'люблю': {'test3.txt': [Position(0, 5, 10)]},
      'красные': {'test3.txt': [Position(0, 11, 18)]},
      'бобы': {'test3.txt': [Position(0, 19, 23),
                             Position(0, 31, 35),
                             Position(0, 38, 42),
                             Position(0, 61, 65),
                             Position(0, 76, 80)]},
      'белые': {'test3.txt': [Position(0, 25, 30)]},
      'и': {'test3.txt': [Position(0, 36, 37)]},
      'вообще': {'test3.txt': [Position(0, 43, 49)]},
      'Противные': {'test3.txt': [Position(0, 51, 60)]},
      'Дурацкие': {'test3.txt': [Position(0, 67, 75)]}}


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

class ContextFromFileTest(unittest.TestCase):
    """This is to test from_file classmethod of class Context"""
    def setUp(self):
        with open("test.txt", 'w') as f:
            f.write(TEST)
        with open("test1.txt", 'w') as f:
            f.write(TEST1)

    def test_wrong_input_error(self):
        with self.assertRaises(ValueError):
            Context.from_file(42, 42, 42)

    def test_output_type(self):
        result = Context.from_file("test1.txt", Position(0, 8, 12), 3)
        self.assertIsInstance(result, Context)

    def test_word_in_the_middle(self):
        result = Context.from_file("test1.txt", Position(0, 16, 20), 2)
        self.assertEqual(result.positions, [Position(0, 16, 20)])
        self.assertEqual(result.start, 8)
        self.assertEqual(result.end, 31)
        self.assertEqual(result.line, TEST1)

    def test_word_in_the_beginning(self):
        result = Context.from_file("test1.txt", Position(0, 8, 12), 3)
        self.assertEqual(result.positions, [Position(0, 8, 12)])
        self.assertEqual(result.start, 0)
        self.assertEqual(result.end, 24)
        self.assertEqual(result.line, TEST1)
        
    def test_word_in_the_end(self):
        result = Context.from_file("test1.txt", Position(0, 32, 38), 3)
        self.assertEqual(result.positions, [Position(0, 32, 38)])
        self.assertEqual(result.start, 16)
        self.assertEqual(result.end, 38)
        self.assertEqual(result.line, TEST1)

    def test_zero_context(self):
        result = Context.from_file("test1.txt", Position(0, 8, 12), 0)
        self.assertEqual(result.positions, [Position(0, 8, 12)])
        self.assertEqual(result.start, 8)
        self.assertEqual(result.end, 12)
        self.assertEqual(result.line, TEST1)

    def test_last_line(self):
        result = Context.from_file("test.txt", Position(1, 14, 20), 2)
        self.assertEqual(result.positions, [Position(1, 14, 20)])
        self.assertEqual(result.start, 6)
        self.assertEqual(result.end, 27)
        self.assertEqual(result.line, "it is to test search engine")

    def test_first_line(self):
        result = Context.from_file("test.txt", Position(0, 8, 9), 0)
        self.assertEqual(result.positions, [Position(0, 8, 9)])
        self.assertEqual(result.start, 8)
        self.assertEqual(result.end, 9)
        self.assertEqual(result.line, "this is a test text")

    def tearDown(self):
        os.remove("test.txt")
        os.remove("test1.txt")

class IntersectContextTest(unittest.TestCase):
    def setUp(self):
        self.se = SearchEngine("test_db")
        self.se.db.update(DB)
        with open("test.txt", 'w') as f:
            f.write(TEST)
        with open("test1.txt", 'w') as f:
            f.write(TEST1)
        with open("test3.txt", 'w') as f:
            f.write(TEST3)
        # a
        self.search_result1 = {'test.txt': [Position(0, 8, 9)]}
        # бобы
        self.search_result2 = {'test3.txt': [Position(0, 19, 23),
                                        Position(0, 31, 35),
                                        Position(0, 38, 42),
                                        Position(0, 61, 65),
                                        Position(0, 76, 80)]}
        # to test
        self.search_result3 = {'test.txt': [Position(0, 10, 14),
                                            Position(1, 6, 8),
                                            Position(1, 9, 13)],
                               'test1.txt': [Position(0, 13, 15),
                                             Position(0, 16, 20)]}

    def test_wrong_input_error(self):
        with self.assertRaises(ValueError):
            self.se.get_context_window(3, 3)
    
    def test_output_type(self):
        result = self.se.get_context_window(self.search_result1, 1)
        self.assertIsInstance(result, dict)
        
    def test_empty_input(self):
        result = self.se.get_context_window({}, 3)
        self.assertEqual(result, {})
        
    def test_zero_context(self):
        result = self.se.get_context_window(self.search_result1, 0)
        ideal = {'test.txt': [Context([Position(0, 8, 9)],
                                                TEST[0:19], 8, 9)]}
        self.assertEqual(result, ideal)
        
    def test_two_words_intersection(self):
        result = self.se.get_context_window(self.search_result3, 2)
        ideal = {'test.txt': [Context([Position(0, 10, 14)],
                                      TEST[0:19], 5, 19),
                              Context([Position(1, 6, 8),
                                       Position(1, 9, 13)],
                                      TEST[20:], 0, 27)],
                 'test1.txt': [Context([Position(0, 13, 15),
                                        Position(0, 16, 20)],
                                       TEST1, 0, 31)]}
        self.assertEqual(result, ideal)

    def test_eq(self):
        a = Context([Position(0, 8, 9)], TEST[0:19], 8, 9)
        b = Context([Position(0, 8, 9)], TEST[0:19], 8, 9)
        self.assertEqual(a,b)

    def test_intersect(self):
        a = Context([Position(0, 13, 15)], TEST1, 0, 24)
        b = Context([Position(0,16,20)], TEST1, 0, 31)
        self.assertEqual(a.intersect(b), Context([Position(0, 13, 15),
                                          Position(0, 16, 20)],
                                         TEST1, 0, 31))


    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)
        os.remove("test.txt")
        os.remove("test1.txt")
        os.remove("test3.txt")

                        
if __name__ == '__main__':
    unittest.main()
