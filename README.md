# What is this?

This module allows to tokenize a string of characters and index files.

### Tokenizer

This class alows to tokenize a string of characters in multiple ways:

1. Return alphabetical tokens only.
2. Divide the whole string into tokens specifying them as belonging to one of the following types:
* a - alphabetic
* d - digit
* s - space
* p - punctuation
* o - other
3. Extract only alphabetical and numerical tokens for use of Indexer.

### Indexer

This class allows to index a file line by line and write the indexes (line, position of first and last characters of the token) and the filename into a database. Thus you can index multiple files into one database.

### SearchEngine

A primitive search engine that returns positions of a given token.

## Why

This module is created as a practical work for my university programming course.


