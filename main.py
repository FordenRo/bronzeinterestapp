import sys
from importlib import import_module
import os
import logging

from client import client, bot
from config import config


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
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    initiate_handlers()

    await bot.send_message((await client.get_me()).id, 'Started')
    logging.info('Started successfully')
    await client.disconnected


if __name__ == '__main__':
    with client:
        try:
            client.loop.run_until_complete(main())
        except KeyboardInterrupt:
            logging.info('Stopping')
            config.save()
