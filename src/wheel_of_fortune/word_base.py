import random


class WordsDB:
    def __init__(self, words_db_path):
        self.words = open(words_db_path).read().split('\n')

    def get_random_word(self):
        return random.choice(self.words)
