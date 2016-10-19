from main import *
from math import sqrt


def main():
    frequentPatterns, tokens = readFileAndFindFrequentPatterns("haluz")
    sentence = "Catching a Baseball: A Reinforcement Learning Perspective Using a Neural Network"
    extractPhrases(frequentPatterns, tokenizeText(sentence), len(tokens))

    sentence1 = 'The Intelligent Database Interface: Integrating AI and Database Systems.'
    extractPhrases(frequentPatterns, tokenizeText(sentence1), len(tokens))

def extractPhrases(frequentPatterns, tokens, stats):
    originalSize = len(tokens)
    ind = 0
    phrases = []
    while ind < originalSize - 1:
        if significanceScore(frequentPatterns, stats, tokens[ind], tokens[ind + 1]) > 1:
            phrases.append(tokens[ind] + " " + tokens[ind + 1])
            # tokens = [(tokens[ind] + " " + tokens[ind + 1])].extend(tokens[ind + 1:])
        ind += 1

    for phr in phrases:
        print phr
    return phrases

def significanceScore(frequentPatterns, vocabSize, phraseLeft, phraseRight):
    if phraseRight not in frequentPatterns:
        rightPhraseCount = 0
    else:
        rightPhraseCount = frequentPatterns[phraseRight]

    if phraseLeft not in frequentPatterns:
        leftPhraseCount = 0
    else:
        leftPhraseCount = frequentPatterns[phraseLeft]


    mergedPhrase = phraseLeft + " " + phraseRight
    if mergedPhrase not in frequentPatterns:
        return 0
    else:
        mergedPhraseCount = frequentPatterns[mergedPhrase]

    return (mergedPhraseCount - (leftPhraseCount * rightPhraseCount) / (vocabSize * vocabSize)) / sqrt(mergedPhraseCount)


if __name__ == "__main__":
    main()