from .translator import Translator
from .word_base import WordsDB


class WOFCore:
    def __init__(self):
        self.translator = Translator("resources/translations/", "config.txt")
        self.word_db = WordsDB("resources/words.txt")

    def generate_word(self) -> str:
        return self.word_db.get_random_word()

    def get_text_line(self, text_line_name) -> str:
        return self.translator.get(text_line_name)


MAIN_CORE = WOFCore()
