import logging
import os
import sys
from importlib import import_module
from io import StringIO
from logging import StreamHandler

from telethon.tl.custom import Message

from client import bot, client
from config import save_config
from utils import TgLogHandler


def initiate_handlers():
    logging.info('Initiating client handlers...')
    for handler in os.listdir('client_handlers'):
        name, ext = os.path.splitext(handler)
        if ext != '.py':
            continue

        logging.info(f'{name} initiated')
        import_module(f'client_handlers.{name}')

    logging.info('Initiating bot handlers...')
    for handler in os.listdir('bot_handlers'):
        name, ext = os.path.splitext(handler)
        if ext != '.py':
            continue

        logging.info(f'{name} initiated')
        import_module(f'bot_handlers.{name}')


async def main():
    bot.parse_mode = 'html'

    if client._self_id is None:
        raise ValueError('client._self_id is None')

    msg = await bot.send_message(client._self_id, 'log')
    if not isinstance(msg, Message):
        raise ValueError('msg is not a Message')

    await bot.pin_message(client._self_id, msg.id)

    stream = StreamHandler(StringIO())
    stream.name = 'Stream'
    logging.basicConfig(level=logging.INFO,
                        format='{asctime} [{levelname}] ({name}) {message}',
                        style='{',
                        datefmt='%H:%M',
                        handlers=[StreamHandler(sys.stdout), TgLogHandler(msg), stream])
    logging.getLogger('telethon.client.updates').setLevel(logging.WARN)

    initiate_handlers()

    logging.info('Started successfully')
    await client.disconnected

    await bot.unpin_message(client._self_id, msg.id)
    logging.info('Stopped')
    save_config()


if __name__ == '__main__':
    with client:
        try:
            client.loop.run_until_complete(main())
        except KeyboardInterrupt:
            logging.info('Stopping')
