import logging
import os
import sys
from importlib import import_module
from logging import StreamHandler

from client import bot, client
from config import config
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
    me = await client.get_me()
    msg = await bot.send_message(me.id, 'log')
    await bot.pin_message(me.id, msg.id)

    logging.basicConfig(level=logging.INFO,
                        format='[{asctime} {levelname}] ({name}) {msg}',
                        style='{',
                        datefmt='%H:%M',
                        handlers=[StreamHandler(sys.stdout), TgLogHandler(msg)])
    logging.getLogger('telethon.client.updates').setLevel(logging.WARN)

    initiate_handlers()

    logging.info('Started successfully')
    await client.disconnected

    await bot.unpin_message(me.id, msg.id)
    logging.info('Stopped')
    config.save()


if __name__ == '__main__':
    with client:
        try:
            client.loop.run_until_complete(main())
        except KeyboardInterrupt:
            logging.info('Stopping')

