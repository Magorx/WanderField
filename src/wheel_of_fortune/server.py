import asyncio
import socket

from .core import MAIN_CORE
from .session import Session


EOL = '\n\r' # end of line
EOM = '\0'   # end of message
END_OF_GAME = '\1' + EOM

def line(text_line_name):
    return MAIN_CORE.get_text_line(text_line_name)


class Server:
    def __init__(self, ip: str, port: int, wrong_letters_count: int):
        self.ip = ip
        self.port = port
        self.wrong_letters_count = wrong_letters_count

    def set_language(self, language):
        MAIN_CORE.translator.set_language(language)

    async def run(self):
        server = await asyncio.start_server(self.handle_client, self.ip, self.port)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer_name = writer.get_extra_info("peername")
        session = Session(reader, writer, MAIN_CORE, self.wrong_letters_count)

        print(f'{peer_name} connected')

        try:
            await session.send(line("welcome") + EOL)

            while not session.is_complete():
                msg = line("current_word") + ' ' + session.get_shown_word() + EOL
                msg = msg + line("letters_left") + ' ' + session.get_letters_left() + EOL
                msg = msg + line("mistakes_left") + ' ' + str(session.wrong_letters_count) + EOL
                msg = msg + EOM
                await session.send(msg)

                data = await reader.readline()
                message = data.decode().rstrip().lower()

                if len(message) > 1:
                    await session.send(line("enter_one_letter") + EOL)
                    continue
                elif message in session.letters_guessed:
                    await session.send(line("letter_already_used") + EOL)
                    continue

                letters_guessed = session.letter_guess(message)

                if letters_guessed == 0:
                    await session.send(line("wrong_letter") + EOL)

                elif letters_guessed == 1:
                    await session.send(line("right_letter_1") + EOL)
                elif letters_guessed == 2:
                    await session.send(line("right_letter_2") + EOL)
                else:
                    await session.send(line("right_letter_many") + EOL)

            await session.send(EOL + line("word_is") + ' ' + session.word + EOL)
            await session.send(session.final_message + EOL + END_OF_GAME)
            session.disconnect_client()

        except socket.error as e:
            print(f'{peer_name} disconnected')
            session.stop()
