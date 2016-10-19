from frequent_mining import *
import sys

def readFileAndFindFrequentPatterns(argv):
    inputTextFile = 'dblp_titles.txt'
    text = open(inputTextFile, 'r')

    tokens = []

    for line in text:
        tokens.extend(tokenizeText(line))

    print "Total number of tokens is: ", len(tokens)
    return findFrequentPatterns(tokens, 50), tokens

def tokenizeText(text):
    PUNCTUATION = ".!?,;:\"[]"
    chars = []
    tokens = []
    for char in text:
        if char.isalpha():
            chars.append(char.lower())
        elif char == '\'':
            chars.append(char)
        elif len(chars) > 0:
            tokens.append(''.join(chars))
            chars = []
        if char in PUNCTUATION:
            tokens.append('$')
    if len(chars) > 0:
        tokens.append(''.join(chars))
        chars = []
    return tokens

if __name__ == "__main__":
    readFileAndFindFrequentPatterns(sys.argv[1 : ])