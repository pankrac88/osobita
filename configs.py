"""Configuration class with all the required config params."""
import logging


class Config:

    LOGGING_LEVEL = logging.INFO
    CORPUS_FILE = './corpus/dblp_titles.txt'
    FREQ_PATTERN_THRESHOLD = 2
    T_SCORE_THRESHOLD = 5
