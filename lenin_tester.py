import unittest
from collections import Generator
from lenin_tokenizer import Tokenizer

class GetTypeTest(unittest.TestCase):
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
        result = self.tokenizer._getType('А')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "a")
    def test_digit(self):
        result = self.tokenizer._getType('0')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "d")
        result = self.tokenizer._getType('1')
        self.assertEqual(len(result), 1)
        self.assertEqual(result, "d")
        result = self.tokenizer._getType('3')
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
        result = self.tokenizer._getType(',')
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
