import unittest
import os
import shelve
from collections.abc import Generator
from lenin_search_engine import SearchEngine, Context
from lenin_indexer import Position
from lenin_search_engine_tester import TEST, TEST1, TEST2, TEST3, DB

class SearchLimitTest(unittest.TestCase):
    def setUp(self):
        self.se = SearchEngine("test_db")
        self.se.db.update(DB)
        with open("test.txt", 'w') as f:
            f.write(TEST)
        with open("test1.txt", 'w') as f:
            f.write(TEST1)
        with open("test3.txt", 'w') as f:
            f.write(TEST3)

    def test_default(self):
        # default limit = 10
        # default offset = 0
        # default doclo = [(3,0),(3,0),(3,0),(3,0),(3,0),(3,0),(3,0),(3,0),(3,0),(3,0)]
        query = "test"
        result = self.se.search_to_quote_limit(query)
        ideal = {'test.txt': ['this is a <b>test</b> text',
                              'it is to <b>test</b> search engine'],
                 'test1.txt': ['another text to <b>test</b> the search engine']}
        self.assertEqual(result, ideal)

    def test_one(self):
        # limit = 1
        # offset = 0
        # doclo = [(1,0)]
        query = "test"
        result = self.se.search_to_quote_limit(query,
                                               limit=1,
                                               offset=0,
                                               doclo=[(1,0)])
        ideal = {'test.txt':
                 ['this is a <b>test</b> text']}
        self.assertEqual(result, ideal)

    def test_two(self):
        # limit = 1
        # offset = 1
        # doclo = [(1,0)]
        query = "test"
        result = self.se.search_to_quote_limit(query,
                                               limit=1,
                                               offset=1,
                                               doclo=[(1,0)])
        ideal = {'test1.txt': ['another text to <b>test</b> the search engine']}
        self.assertEqual(result, ideal)

    def test_three(self):
        # limit = 0
        # offset = 1
        # doclo = [(1,0)]
        query = "test"
        result = self.se.search_to_quote_limit(query,
                                               limit=0,
                                               offset=1,
                                               doclo=[(1,0)])
        ideal = {}
        self.assertEqual(result, ideal)

    def test_four(self):
        # limit = 2
        # offset = 1
        # doclo = [(3,1), (3,0)]
        query = "test"
        result = self.se.search_to_quote_limit(query,
                                      limit=2,
                                      offset=1,
                                      doclo=[(3,1), (3,0)])
        ideal = {'test1.txt': []}
        self.assertEqual(result, ideal)

    def test_five(self):
        # limit = 2
        # offset = 2
        # doclo = [(3,1), (3,0)]
        query = "test"
        result = self.se.search_to_quote_limit(query,
                                               limit=2,
                                               offset=2,
                                               doclo=[(3,1), (3,0)])
        ideal = {}
        self.assertEqual(result, ideal)

    def test_six(self):
        # limit = 2
        # offset = 0
        # doclo = [(3,1),(3,0)]
        query = "test"
        result = self.se.search_to_quote_limit(query,
                                               limit=2,
                                               offset=0,
                                               doclo=[(3,1), (3,0)])
        ideal = {'test.txt': ['it is to <b>test</b> search engine'],
                 'test1.txt': ['another text to <b>test</b> the search engine']}
        self.assertEqual(result, ideal)
            
    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)
        os.remove("test.txt")
        os.remove("test1.txt")
        os.remove("test3.txt")

class MultiwordSearchLimitDocTest(unittest.TestCase):
    """
    Tests method multiword_search of SearchEngine.
    """
    def setUp(self):
        self.se = SearchEngine("test_db")
        self.se.db.update(DB)

    def test_wrong_input_error(self):
        with self.assertRaises(ValueError):
            self.se.multiword_search_limit_doc(123)

    def test_empty_input(self):
        result = self.se.multiword_search_limit_doc("")
        self.assertEqual(result, {})

    def test_no_alph_or_num_in_input(self):
        result = self.se.multiword_search_limit_doc("!!!")
        self.assertEqual(result, {})

    def test_absent_key(self):
        result = self.se.multiword_search_limit_doc("turtle test")
        self.assertEqual(result, {})

    def test_adjacent_words(self):
        result = self.se.multiword_search_limit_doc("to test")
        self.assertEqual(result, {'test.txt': [Position(0, 10, 14),
                                               Position(1, 6, 8),
                                               Position(1, 9, 13)],
                                  'test1.txt': [Position(0, 13, 15),
                                                Position(0, 16, 20)]})
        
    def test_far_words(self):
        result = self.se.multiword_search_limit_doc("cat animals")
        self.assertEqual(result, {'test2.txt': [Position(0, 0, 3),
                                                Position(5, 10, 17)]})
    def test_offset(self):
        result = self.se.multiword_search_limit_doc("to test", offset=1)
        self.assertEqual(result, {'test1.txt': [Position(0, 13, 15),
                                                Position(0, 16, 20)]})
    def test_limit(self):
        result = self.se.multiword_search_limit_doc("to test", limit=1)
        self.assertEqual(result, {'test.txt': [Position(0, 10, 14),
                                               Position(1, 6, 8),
                                               Position(1, 9, 13)]})
    def test_zero_limit(self):
        result = self.se.multiword_search_limit_doc("to test", limit=0)
        self.assertEqual(result, {})

    def test_neg_limit(self):
        result = self.se.multiword_search_limit_doc("to test", limit=-1)
        self.assertEqual(result, {})

    def test_neg_offset(self):
        result = self.se.multiword_search_limit_doc("to test", offset=-10)
        self.assertEqual(result, {'test.txt': [Position(0, 10, 14),
                                               Position(1, 6, 8),
                                               Position(1, 9, 13)],
                                  'test1.txt': [Position(0, 13, 15),
                                                Position(0, 16, 20)]})
    def test_neg_offset_limit(self):
        result = self.se.multiword_search_limit_doc("to test", limit=1, offset=-2)
        self.assertEqual(result, {'test.txt': [Position(0, 10, 14),
                                               Position(1, 6, 8),
                                               Position(1, 9, 13)]})
    def test_over_offset(self):
        result = self.se.multiword_search_limit_doc("to test", offset=4)
        self.assertEqual(result, {})

    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)

class PositionGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.se = SearchEngine("test_db")
        self.se.db.update(DB)
        
    def test_generator(self):
        lists = [[1, 3, 5, 7, 9],
                 [2, 4, 45, 80]]
        ideal = [1, 2, 3, 4, 5, 7, 9, 45, 80]
        result = list(self.se.position_generator(lists))
        self.assertEqual(result, ideal)

    def test_generator1(self):
        lists = [[1, 2, 3, 4],
                 [5, 7, 9, 45]]
        ideal = [1, 2, 3, 4, 5, 7, 9, 45]
        result = list(self.se.position_generator(lists))
        self.assertEqual(result, ideal)

    def test_position(self):
        lists = [[Position(10, 4, 5), Position(40, 0, 5)],
                 [Position(0, 0, 2), Position(10, 3, 4), Position(40, 6, 8)]]
        ideal = [Position(0, 0, 2), Position(10, 3, 4), Position(10, 4, 5),
                 Position(40, 0, 5), Position(40, 6, 8)]
        result = list(self.se.position_generator(lists))
        self.assertEqual(result, ideal)

    def test_search(self):
        result = self.se.multiword_search_gen("to test", limit=1, offset=-2)
        self.assertIsInstance(result['test.txt'], Generator)

    def test_wrong_input_error(self):
        with self.assertRaises(ValueError):
            self.se.multiword_search_gen(123)

    def test_empty_input(self):
        result = self.se.multiword_search_gen("")
        self.assertEqual(result, {})

    def test_no_alph_or_num_in_input(self):
        result = self.se.multiword_search_gen("!!!")
        self.assertEqual(result, {})

    def test_absent_key(self):
        result = self.se.multiword_search_gen("turtle test")
        self.assertEqual(result, {})

    def test_adjacent_words(self):
        result = self.se.multiword_search_gen("to test")
        ideal = {'test.txt': [Position(0, 10, 14),
                               Position(1, 6, 8),
                               Position(1, 9, 13)],
                  'test1.txt': [Position(0, 13, 15),
                                Position(0, 16, 20)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])
        
    def test_far_words(self):
        result = self.se.multiword_search_gen("cat animals")
        ideal = {'test2.txt': [Position(0, 0, 3), Position(5, 10, 17)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])
            
    def test_offset(self):
        result = self.se.multiword_search_gen("to test", offset=1)
        ideal = {'test1.txt': [Position(0, 13, 15), Position(0, 16, 20)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])
            
    def test_limit(self):
        result = self.se.multiword_search_gen("to test", limit=1)
        ideal = {'test.txt': [Position(0, 10, 14),
                              Position(1, 6, 8),
                              Position(1, 9, 13)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])
            
    def test_zero_limit(self):
        result = self.se.multiword_search_gen("to test", limit=0)
        self.assertEqual(result, {})

    def test_neg_limit(self):
        result = self.se.multiword_search_gen("to test", limit=-1)
        self.assertEqual(result, {})

    def test_neg_offset(self):
        result = self.se.multiword_search_gen("to test", offset=-10)
        ideal = {'test.txt': [Position(0, 10, 14),
                                               Position(1, 6, 8),
                                               Position(1, 9, 13)],
                                  'test1.txt': [Position(0, 13, 15),
                                                Position(0, 16, 20)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])
            
    def test_neg_offset_limit(self):
        result = self.se.multiword_search_gen("to test", limit=1, offset=-2)
        ideal = {'test.txt': [Position(0, 10, 14),
                                               Position(1, 6, 8),
                                               Position(1, 9, 13)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])
            
    def test_over_offset(self):
        result = self.se.multiword_search_gen("to test", offset=4)
        self.assertEqual(result, {})
                 

    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)


class ContextGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.se = SearchEngine("test_db")
        self.se.db.update(DB)
        with open("test.txt", 'w') as f:
            f.write(TEST)
        with open("test1.txt", 'w') as f:
            f.write(TEST1)

    def test_generator(self):
        pos = [Position(0, 10, 14), Position(1, 9, 13)]
        result = list(self.se.context_generator("test.txt", pos, 2))
        ideal = [Context([Position(0, 10, 14)], TEST[:19], 5, 19),
                 Context([Position(1, 9, 13)], TEST[20:], 3, 27)]
        self.assertEqual(result, ideal)

    def test_generator2(self):
        pos = [Position(0, 0, 4), Position(0, 5, 7)]
        result = list(self.se.context_generator("test.txt", pos, 1))
        ideal = [Context([Position(0, 0, 4), Position(0, 5, 7)],
                         TEST[:19], 0, 9)]
        self.assertEqual(result, ideal)

    def text_generator3(self):
        pos = [Position(0, 0, 4), Position(0, 10, 14), Position(1, 0, 2),
               Position(1, 3, 5), Position (1, 14, 20)]
        result = list(self.se.context_generator("test.txt", pos, 1))
        ideal = [Context([Position(0, 0, 4)], TEST[:19], 0, 7),
                 Context([Position(0, 10, 14)], TEST[:19], 8, 19),
                 Context([Position(1, 0, 2), Position(1, 3, 5)],
                         TEST[20:], 0, 8),
                 Context([Position(1, 14, 20)], TEST[20:], 9, 27)]
        self.assertEqual(result, ideal)

    def test_search_to_context(self):
        result = self.se.search_to_context_gen("to test")
        ideal = {'test.txt': [Context([Position(0, 10, 14)], TEST[:19], 0, 19),
                              Context([Position(1, 6, 8),
                                       Position(1, 9, 13)], TEST[20:], 0, 27)],
                 'test1.txt': [Context([Position(0, 13, 15),
                                        Position(0, 16, 20)], TEST1, 0, 38)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])
        
    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)
        os.remove("test.txt")
        os.remove("test1.txt")


class SentnceGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.se = SearchEngine("test_db")
        self.se.db.update(DB)
        with open("test3.txt", 'w') as f:
            f.write(TEST3)
        
    def test_join_two_contexts(self):
        # вообще Дурацкие
        con = [Context([Position(0, 43, 49)], TEST3, 0, 66),
               Context([Position(0, 67, 75)], TEST3, 51, 81)]
        ideal = [Context([Position(0, 43, 49), Position(0, 67, 75)],
                         TEST3, 0, 81)]
        result = list(self.se.sentence_generator(con))
        self.assertEqual(result, ideal)
        

    def test_search_to_sentence(self):
        query = "Дурацкие вообще"
        result = self.se.search_to_sentence_gen(query)
        ideal = {'test3.txt': [Context([Position(0, 43, 49),
                                        Position(0, 67, 75)],
                                       TEST3, 0, 81)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])

    def test_search_to_sentence_2(self):
        query = "Я Дурацкие"
        result = self.se.search_to_sentence_gen(query, 0)
        ideal = {'test3.txt': [Context([Position(0, 0, 1)], TEST3, 0, 50),
                               Context([Position(0, 67, 75)], TEST3, 67, 81)]}
        for f in result:
            self.assertEqual(list(result[f]), ideal[f])
            
    def tearDown(self):
        del self.se
        for filename in os.listdir('.'):
            if filename.startswith("test_db."):
                os.remove(filename)
        os.remove("test3.txt")


if __name__ == '__main__':
    unittest.main()
