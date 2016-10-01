from frequent_mining import *
import sys

def main(argv):
    PUNCTUATION = ".!?,;:\"[]"
    inputTextFile = 'dblp_titles.txt'
    text = open(inputTextFile, 'r')

    tokens = []

    for line in text:
        chars = []

        for char in line:
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

    print "Total number of tokens is: ", len(tokens)
    findFrequentPatterns(tokens, 50)

if __name__ == "__main__":
    main(sys.argv[1 : ])