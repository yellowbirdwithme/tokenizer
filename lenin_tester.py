import unittest
from collections import Generator
from lenin_tokenizer import Tokenizer

class GenerateTest(unittest.TestCase):
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

    def test_Error_wrong_input_number(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize(42)
            
    def test_Error_wrong_input_list(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize(['this', 'is', 'a', 'trap'])    

if __name__ == '__main__':
    unittest.main()
