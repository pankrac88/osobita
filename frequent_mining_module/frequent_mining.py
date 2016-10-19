def printTokens(tokens):
    for token in tokens:
        print(token)


def findFrequentPatterns(tokens, minFreqThreshold):

    tokenIndex = {}
    # CALCULATES FREQUENCIES OF TOKENS IN THE CORPUS
    for index in xrange(len(tokens)):
        token = tokens[index]
        if token in tokenIndex:
            tokenIndex[token].append(index)
        else:
            tokenIndex[token] = [index]

    patternLength = 1
    frequentPatterns = {}
    while(len(tokenIndex) > 0):
        if patternLength > 4:
            break
        patternLength += 1
        newPatternIndex = {}

        for token, positions in tokenIndex.items():
            if len(positions) > minFreqThreshold:
                frequentPatterns[token] = len(positions)
            for position in positions:
                if position + 1 < len(tokens):
                    if tokens[position + 1] == "$":
                        continue
                    newPattern = token + " " + tokens[position + 1]
                    if newPattern in newPatternIndex:
                        newPatternIndex[newPattern].append(position + 1)
                    else:
                        newPatternIndex[newPattern] = [position + 1]

        tokenIndex.clear()
        tokenIndex = newPatternIndex

    for phrase in frequentPatterns:
        print phrase, frequentPatterns[phrase]

    return frequentPatterns




