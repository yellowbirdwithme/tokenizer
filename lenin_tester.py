import unittest
import os
import shelve
from collections import Generator
from lenin_tokenizer import Tokenizer, Indexer, Position


class GetTypeTest(unittest.TestCase):
    """
    Tests private method _getType of class Tokenizer
    """
    def setUp(self):
        self.tokenizer = Tokenizer()
        
    def test_alpa_latina(self):
        result = self.tokenizer._getType('c')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "a")
        result = self.tokenizer._getType('Z')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "a")

    def test_alpa_russa(self):
        result = self.tokenizer._getType('а')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "a")
        result = self.tokenizer._getType('Ё')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "a")
        result = self.tokenizer._getType('ё')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "a")
        result = self.tokenizer._getType('Я')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "a")

    def test_digit(self):
        result = self.tokenizer._getType('0')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "d")
        result = self.tokenizer._getType('9')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "d")

    def test_space(self):
        result = self.tokenizer._getType(' ')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "s")

    def test_punct(self):
        result = self.tokenizer._getType('.')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "p")
        result = self.tokenizer._getType('!')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "p")
        result = self.tokenizer._getType('¿')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "p")
        result = self.tokenizer._getType('/')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "p")
        result = self.tokenizer._getType(')')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "p")


class GenerateWithTypeTest(unittest.TestCase):
    """
    Tests method generate_with_type of class Tokenizer
    """
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_output_type(self):
        result = self.tokenizer.generate_with_type('test')
        self.assertIsInstance(result, Generator)

    def test_alpha_and_spaces_only(self):
        result = list(self.tokenizer.generate_with_type('I am very tired'))
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[0].tp, 'a')
        self.assertEqual(result[1].s, ' ')
        self.assertEqual(result[1].pos, 1)
        self.assertEqual(result[1].tp, 's')
        self.assertEqual(result[6].s, 'tired')
        self.assertEqual(result[6].pos, 10)
        self.assertEqual(result[6].tp, 'a')

    def test_all_types_of_character(self):
        result = list(self.tokenizer.generate_with_type(
            'I am very  tired, I want to go to sleep at 6:30!!!'))
        self.assertEqual(len(result), 27)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[0].tp, 'a')
        self.assertEqual(result[5].s, '  ')
        self.assertEqual(result[5].pos, 9)
        self.assertEqual(result[5].tp, 's')
        self.assertEqual(result[7].s, ',')
        self.assertEqual(result[7].pos, 16)
        self.assertEqual(result[7].tp, 'p')
        self.assertEqual(result[23].s, '6')
        self.assertEqual(result[23].pos, 43)
        self.assertEqual(result[23].tp, 'd')
        self.assertEqual(result[25].s, '30')
        self.assertEqual(result[25].pos, 45)
        self.assertEqual(result[25].tp, 'd')
        self.assertEqual(result[26].s, '!!!')
        self.assertEqual(result[26].pos, 47)
        self.assertEqual(result[26].tp, 'p')

    def test_empty_string(self):
        result = list(self.tokenizer.generate(""))
        self.assertEqual(len(result), 0)

    def test_error_wrong_input_number(self):
        with self.assertRaises(ValueError):
            list(self.tokenizer.generate(42))
            
    def test_error_wrong_input_list(self):
        with self.assertRaises(ValueError):
            list(self.tokenizer.generate(['this', 'is', 'a', 'trap']))


class GenerateTest(unittest.TestCase):
    """
    Tests method generate of class Tokenizer
    """
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_output_type(self):
        result = self.tokenizer.generate('test.')
        self.assertIsInstance(result, Generator)
        
    # default sentence is StartAlphaEndNonAlpha, which represents normal
    # sentence punctuation. In each test it is modified according to the test
    # name. So if the module being tested fails all tests except EndAlpha,
    # the module probably cannot manage sentences ending with non-alphabetic
    # symbols.
    
    def test_start_alpha(self):
        result = list(self.tokenizer.generate('I am very tired Я очень устала.'))
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 24)
        
    def test_start_non_alpha(self):
        result = list(self.tokenizer.generate('.I am very tired Я очень устала.'))
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 1)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 25)
        
    def test_start_multiple_non_alpha(self):
        result = list(self.tokenizer.generate('...I am very tired Я очень устала.'))
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 3)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 27)
        
    def test_middle_multiple_non_alpha(self):
        result = list(self.tokenizer.generate('I am very tired... Я очень устала.'))
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[4].s, 'Я')
        self.assertEqual(result[4].pos, 19)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 27)
        
    def test_end_alpha(self):
        result = list(self.tokenizer.generate('I am very tired Я очень устала'))
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 24)

    def test_end_multiple_non_alpha(self):
        result = list(self.tokenizer.generate('I am very tired Я очень устала :((('))
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 24)

    def test_empty_string(self):
        result = list(self.tokenizer.generate(""))
        self.assertEqual(len(result), 0)

    def test_error_wrong_input_number(self):
        with self.assertRaises(ValueError):
            list(self.tokenizer.generate(42))
            
    def test_error_wrong_input_list(self):
        with self.assertRaises(ValueError):
            list(self.tokenizer.generate(['this', 'is', 'a', 'trap']))

            
class TokenizeTest(unittest.TestCase):
    """
    Tests method tokenize of class Tokenizer
    """
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_output_type(self):
        result = self.tokenizer.tokenize('test.')
        self.assertIsInstance(result, list)
        
    # default sentence is StartAlphaEndNonAlpha, which represents normal
    # sentence punctuation. In each test it is modified according to the test
    # name. So if the module being tested fails all tests except EndAlpha,
    # the module probably cannot manage sentences ending with non-alphabetic
    # symbols.
    
    def test_start_alpha(self):
        result = self.tokenizer.tokenize('I am very tired Я очень устала.')
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 24)
        
    def test_start_non_alpha(self):
        result = self.tokenizer.tokenize('.I am very tired Я очень устала.')
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 1)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 25)
        
    def test_start_multiple_non_alpha(self):
        result = self.tokenizer.tokenize('...I am very tired Я очень устала.')
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 3)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 27)
        
    def test_middle_multiple_non_alpha(self):
        result = self.tokenizer.tokenize('I am very tired... Я очень устала.')
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[4].s, 'Я')
        self.assertEqual(result[4].pos, 19)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 27)
        
    def test_end_alpha(self):
        result = self.tokenizer.tokenize('I am very tired Я очень устала')
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 24)

    def test_end_multiple_non_alpha(self):
        result = self.tokenizer.tokenize('I am very tired Я очень устала :(((')
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[6].s, 'устала')
        self.assertEqual(result[6].pos, 24)

    def test_empty_string(self):
        result = self.tokenizer.tokenize("")
        self.assertEqual(len(result), 0)

    def test_error_wrong_input_number(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize(42)
            
    def test_error_wrong_input_list(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize(['this', 'is', 'a', 'trap'])    


class GenerateWordsAndNumbersTest(unittest.TestCase):
    """
    Tests method generate_words_and_numbers of class Tokenizer
    """
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_all_types_of_token(self):
        result = list(self.tokenizer.generate_words_and_numbers(
            "I am very  tired, I want to go to sleep at 6:30!!!"))
        self.assertEqual(len(result), 13)
        self.assertEqual(result[0].s, 'I')
        self.assertEqual(result[0].pos, 0)
        self.assertEqual(result[1].s, 'am')
        self.assertEqual(result[1].pos, 2)
        self.assertEqual(result[11].s, '6')
        self.assertEqual(result[11].pos, 43)
        self.assertEqual(result[12].s, '30')
        self.assertEqual(result[12].pos, 45)
        
        

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
                         {'test':{'test.txt':[Position(0,4,0)]}})
        
    def test_two_identical_words(self):
        with open("test.txt", 'tw') as f:
            f.write("test test")
        self.indexer.index("test.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'test':{'test.txt':[Position(0,4,0), Position(5,9,0)]}})
        
    def test_two_different_words(self):
        with open("test.txt", 'tw') as f:
            f.write("test case")
        self.indexer.index("test.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'test':{'test.txt':[Position(0,4,0)]},
                          'case':{'test.txt':[Position(5,9,0)]}})

    def test_two_files(self):
        with open("test.txt", 'tw') as f:
            f.write("file one")
        with open("test1.txt", 'tw') as f:
            f.write("file two")
        self.indexer.index("test.txt")
        self.indexer.index("test1.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'file':{'test.txt':[Position(0,4,0)],
                                  'test1.txt':[Position(0,4,0)]},
                          'one':{'test.txt':[Position(5,8,0)]},
                          'two':{'test1.txt':[Position(5,8,0)]}})

    def test_multiple_lines(self):
        with open("test.txt", 'tw') as f:
            f.write("""test\nme\nplease""")
        self.indexer.index("test.txt")
        self.assertEqual(dict(self.indexer.db),
                         {'test':{'test.txt':[Position(0,4,0)]},
                          'me':{'test.txt':[Position(0,2,1)]},
                          'please':{'test.txt':[Position(0,6,2)]}})
        
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
