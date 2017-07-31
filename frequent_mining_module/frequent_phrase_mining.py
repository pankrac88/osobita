import collections
from flask import current_app


def findFrequentPhrases(inputTextFile, minFreqThreshold):
    """Find frequently occuring phrases from the corpus file.
 
    The method reads the corpus file where each line is one document,
    The frequent patter mining algorithm is applied to find frequently
    occuring phrases.

    minFreqThreshold param: determines when a pattern becomes frequent.
    """
    documents = {}
    indices = {}
    docId = 0
    termCounts = collections.Counter()
    vocab_size = 0

    with open(inputTextFile, 'r') as corpus:
        for document in corpus:
            # TODO: Use proper tokenizer
            documentTokens = tokenizeText(document)
            vocab_size += len(documentTokens)
            documents[docId] = documentTokens
            indices[docId] = range(len(documentTokens))
            termCounts.update(documentTokens)
            docId += 1
  
    if not documents:
        raise RuntimeError(
            'No corpus data were loaded - pls provide proper corpus file!'
            )
    n = 2
    while len(documents) > 0:
        for docId in list(documents.keys()):
            indices[docId] = [
                ind for ind in indices[docId]
                if (termCounts[' '.join(documents[docId][ind:ind + n - 1])] >
                    minFreqThreshold)
            ]

            if not indices[docId]:
                indices.pop(docId, None)
                documents.pop(docId, None)
                continue
            else:
                for index in indices[docId]:
                    if index + 1 in indices[docId]:
                        phrase = ' '.join(documents[docId][index:index + n])
                        termCounts.update([phrase])
            indices[docId].pop()
        n = n + 1
  
    return termCounts, vocab_size


def tokenizeText(text):
    """Temporary tokenizer - should be replaced."""
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
