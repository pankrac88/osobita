"""Phrase collocation functions."""
import math


def t_score(left_phrase, right_phrase, counter, vocab_size):
    """Generalized t-score as described in []."""
    merged_phrase = ' '.join((left_phrase, right_phrase))
    if merged_phrase not in counter:
        return -math.inf
    actual_freq = counter[merged_phrase]
    expected_freq = (counter[left_phrase] *
                     counter[left_phrase]) / vocab_size

    return actual_freq - expected_freq / math.sqrt(actual_freq)