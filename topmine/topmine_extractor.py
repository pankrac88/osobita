'''This is new implementation of TOPMINE algorithm.'''
from heapq import heappush, heappop
from functools import total_ordering
from flask import current_app


from .scoring_fuctions import t_score


@total_ordering
class Token(object):
    """
    Token representation in the sentence.
    The token has its predecessor and successor.
    This allows easier iteration through the tokens when extracting phrases.
    """
    def __init__(self, data=None, next_token=None, prev_token=None):
        self.data = data
        self.next_token = next_token
        self.prev_token = prev_token

    def get_token(self):
        return self.data.lower()

    def get_next(self):
        """Return successor token of the current one."""
        return self.next_token

    def get_prev(self):
        """Return predecessor token of the current one."""
        return self.prev_token

    def is_phrase(self):
        return ' ' in self.data

    def set_next_token(self, new_token_next):
        self.next_token = new_token_next

    def set_prev_token(self, new_token_prev):
        self.prev_token = new_token_prev

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.data < other.data
        return NotImplemented


class LinkedList(object):
    """
    Simple linkedlist implementation for storing tokens from the sentence.
    It assumes that the list is always populated
    from the beginning of the sentence.
    """
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def insert(self, data):
        """Inserting new token at the end of the list."""
        new_token = Token(data)
        if self.head is None:
            self.head = new_token
            self.tail = new_token
        else:
            prev_token = self.tail
            prev_token.set_next_token(new_token)
            new_token.set_prev_token(prev_token)
            self.tail = new_token

    def merge(self, left_phrase, right_phrase):
        """Merging two existing tokens into one phrase.
        The predecessor of the new phrase is left_phrase.get_prev().
        The successor of the new phrase is right_phrase.get_next()."""
        merged_token = Token('{} {}'.format(left_phrase.get_token(),
                                            right_phrase.get_token()),
                             next_token=right_phrase.get_next(),
                             prev_token=left_phrase.get_prev())
        previous = left_phrase.get_prev()
        previous.set_next_token(merged_token)
        return merged_token

    def size(self):
        """Returns size of the linked list."""
        current = self.head
        size = 0

        while current:
            size += 1
            print('{}'.format(current.get_token()))
            current = current.get_next()
        return size

    def get_phrases(self):
        """Returns only phrases from the linked list - omits unigrams."""
        current = self.head
        phrases = []

        while current:
            if current.is_phrase():
                phrases.append(current.get_token())
            current = current.get_next()
        return phrases

    def stats(self):
        """Provides some info on linked list tokens."""
        print('Head of list is {}'.format(self.head.get_token()))
        print('Tail of list is {}'.format(self.tail.get_token()))
        print('Size of list is {}'.format(self.size()))


significance_score = t_score


def extract_phrases_from_doc(document, counter, vocab_size):
    tokens = document.split(' ')
    document_as_list = LinkedList()

    for ind, token in enumerate(tokens):
        document_as_list.insert(token)

    currentToken = document_as_list.head
    phrase_cands_by_significance = []
    while currentToken.get_next():
        heappush(phrase_cands_by_significance,
                 (invert_score(
                     significance_score(
                        currentToken.get_token(),
                        currentToken.get_next().get_token(),
                        counter, vocab_size)),
                     currentToken, currentToken.get_next()))
        currentToken = currentToken.get_next()

    while len(phrase_cands_by_significance) > 0:
        best_cand = heappop(phrase_cands_by_significance)
        current_app.logger.info('{} {} - score: {}'
                                .format(best_cand[1].get_token(),
                                        best_cand[2].get_token(),
                                        invert_score(best_cand[0])))
        if invert_score(best_cand[0]) > current_app.config['T_SCORE_THRESHOLD']:
            merged_token = document_as_list.merge(best_cand[1], best_cand[2])
            get_candidates_for_merged_phrase(merged_token,
                                             phrase_cands_by_significance,
                                             counter, vocab_size)

    current_app.logger.info(document_as_list.stats())
    return document_as_list.get_phrases()


def invert_score(score):
    """This is workaround function to make from heapq a max heap."""
    return -score


def get_candidates_for_merged_phrase(merged_phrase, cands_by_significance,
                                     counter, vocab_size):
    """After two tokens are merged -> generate
    new candidates from the new merge phrase."""
    right_phrase = merged_phrase.get_next()
    left_phrase = merged_phrase.get_prev()
    # TODO: are there smarter ways of pushing into the queue
    # than doing it everytime?
    if right_phrase:
                heappush(cands_by_significance,
                         (-significance_score(merged_phrase.get_token(),
                                              right_phrase.get_token(),
                                              counter, vocab_size),
                          merged_phrase, right_phrase))
    if left_phrase:
                heappush(cands_by_significance,
                         (-significance_score(left_phrase.get_token(),
                                              merged_phrase.get_token(),
                                              counter, vocab_size),
                          left_phrase, merged_phrase))


if __name__ == '__main__':
    main()


