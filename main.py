import sys
from importlib import import_module
import os
import logging

from client import client

def initiate_handlers():
    logging.getLogger().info('Initiating handlers...')
    for handler in os.listdir('handlers'):
        name, ext = os.path.splitext(handler)
        if ext != '.py':
            continue

        logging.getLogger().info(f'{name} initiated')
        import_module(f'handlers.{name}')


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    initiate_handlers()
    logging.getLogger().info('Started successfully')
    await client.disconnected


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
