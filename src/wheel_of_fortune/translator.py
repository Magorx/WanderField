TEXT_LINE_NAMES = [
    "welcome",              # message a servers sends when a client joins
    "letters_left",         # letters not used by player message
    "mistakes_left",        # how many more fails are allowed for the player
    "current_word",         # current word message
    "enter_one_letter",     # player tried to input more than 1 letter
    "right_letter_1",       # player opened one letter with his guess
    "right_letter_2",       # player opened two letters with his guess
    "right_letter_many",    # player opened more than two letters with his guess
    "wrong_letter",         # player's letter guess was wrong
    "word_guessed",         # player named the whole word by a single guess
    "wrong_letters_loss",   # player ran out of wrong guess tries
    "letter_already_used",  #
    "word_is"               #
]


class Translator:
    def __init__(self, loc_path, config_path):
        self.cur_language = 'en'
        self.languages = {}
        self.loc_path = loc_path

        if not config_path:
            return

        config = open(self.loc_path + config_path).readlines()
        for line in config:
            lang, dir_path = line.split()
            self._load_translation(lang, dir_path)

    def _load_translation(self, lang, dir_path):
        text_lines = {}
        for text_line_name in TEXT_LINE_NAMES:
            text_line_path = self.loc_path + dir_path + text_line_name + '.txt'
            text_line = open(text_line_path, encoding="utf-8").read()
            text_lines[text_line_name] = text_line

        self.languages[lang] = text_lines

    def get(self, text_line_name) -> str:
        if text_line_name in self.languages[self.cur_language]:
            return self.languages[self.cur_language][text_line_name]
        else:
            return "ERROR-TEXT-LINE"

    def set_language(self, language):
        if language in self.languages:
            self.cur_language = language
        else:
            raise Exception("No such language was loaded.")
