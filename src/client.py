import argparse
import asyncio


DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 10001


class TextRadioClient():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.reader = None
        self.writer = None

    async def send(self, msg, to_drain=True):
        msg = msg + '\n'
        msg = msg.encode()
        self.writer.write(msg)
        if to_drain:
            await self.writer.drain()

    async def run(self):
        self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)

        data = await self.reader.readuntil(b'\0')
        msg = data.decode()
        print(msg)

        try:
            while True:
                msg = input("> ")
                await self.send(msg)

                data = await self.reader.readuntil(b'\0')
                msg = data.decode()
                print('\n' + msg)

                if msg[-2] == '\1':     # end of game
                    break
        except Exception as e:
            print("Connection failed.")

async def main():
    parser = argparse.ArgumentParser(description='Wheel of fortune game | CLIENT')

    parser.add_argument('-i', '--ip', dest='ip', default=DEFAULT_IP, type=str)
    parser.add_argument('-p', '--port', dest='port', default=DEFAULT_PORT, type=int)

    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    wof_client = TextRadioClient(args.ip, args.port)
    await wof_client.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print("Game ended abruptly, sorry.")
