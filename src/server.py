import argparse
import asyncio

import wheel_of_fortune as wof


DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 10001


async def main():
    parser = argparse.ArgumentParser(description='Wheel of fortune game | SERVER')

    parser.add_argument('-i', '--ip', dest='ip', default=DEFAULT_IP, type=str)
    parser.add_argument('-p', '--port', dest='port', default=10001, type=int)
    parser.add_argument('-f', '--fails_count', dest='fails_count', default=7, type=int)
    parser.add_argument('-l', '--language', dest='language', default='en', type=str)

    args = parser.parse_args()

    wof_server = wof.Server(DEFAULT_IP, args.port, args.fails_count)
    wof_server.set_language(args.language)

    await wof_server.run()


if __name__ == '__main__':
    asyncio.run(main())
