# What is this?

This module allows to tokenize a string of characters.

# Classes 

### Token

Token is a word that consists solely of alphabetic characters. It has attributes:

s (str): string represention of the token.
  
pos (int): position of the first character of the token.
  
       
### Tokenizer

Class tokenizer that can tokenize a string using method tokenize or generate.

#### method tokenize

Divides a string into Token instances consisting of alphabetic symbols.

Args:

  text (str): String to be tokenized.   
  
Returns:

  List of Token instances.
  
#### method generate

Also divides a string into Token instances consisting of alphabetic symbols as the method tokenize does. 
The difference is that it is a Generator and yields Tokens as soon as it finds them.

Args:
 
text (str): String to be tokenized.

Yields:

Token instances.

## Why

This module is created as a practical work for my university programming course.


