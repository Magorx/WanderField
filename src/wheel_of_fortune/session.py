import string


class Session:
    def __init__(self, reader, writer, core, wrong_letters_count):
        self.reader = reader
        self.writer = writer

        self.core = core
        self.wrong_letters_count = wrong_letters_count
        self.final_message = ''

        self.is_running = True
        self.guessed_letters = []

        self.word = core.generate_word()
        self.word_shown = ['*' for _ in range(len(self.word))]
        self.letters_guessed = set()

    def stop(self, message="The game session was stopped by the server"):
        self.is_running = False
        self.final_message = message

    def letter_guess(self, letter) -> int:
        if len(letter) > 1:
            return 0

        self.letters_guessed.add(letter)

        guessed_cnt = 0
        for i in range(len(self.word)):
            if self.word[i] == letter:
                self.word_shown[i] = letter
                guessed_cnt += 1

        if self.is_complete():
            self.stop(self.core.get_text_line("word_guessed"))
        elif guessed_cnt == 0:
            self.wrong_letters_count -= 1
            if self.wrong_letters_count == 0:
                self.stop(self.core.get_text_line("wrong_letters_loss"))

        return guessed_cnt

    def get_shown_word(self) -> str:
        return ''.join(self.word_shown)

    def get_letters_left(self):
        letters = []
        for c in string.ascii_lowercase:
            if c not in self.letters_guessed:
                letters.append(c)
        return ' '.join(letters)

    def is_complete(self) -> bool:
        if not self.is_running:
            return True

        if self.word_shown.count('*') == 0:
            return True
        else:
            return False

    def disconnect_client(self):
        self.writer.close()

    async def send(self, msg, to_drain=True):
        msg = msg.encode()
        self.writer.write(msg)
        if to_drain:
            await self.writer.drain()