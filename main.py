import logging
import os
import sys
from importlib import import_module
from io import StringIO
from logging import StreamHandler

from telethon.tl.custom import Message
from telethon.tl.types import InputMessagesFilterPinned, User

from client import bot, client
from config import save_config
from handlers.bot.system_commands import get_update_log
from handlers.bot.log_handler import BotLogHandler


def initiate_handlers():
    logging.info('Initiating handlers...')
    for root, _, files in os.walk('handlers'):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext != '.py':
                continue

            logging.getLogger(root.replace(os.sep, '.')).info(f'{name}...')
            import_module(f'{root.replace(os.sep, ".")}.{name}')


async def main():
    bot.parse_mode = 'html'
    client.parse_mode = 'html'

    if client._self_id is None:
        raise ValueError('client._self_id is None')

    if bot._self_id is None:
        raise ValueError('bot._self_id is None')

    pinned_messages = await client.get_messages(bot._self_id, filter=InputMessagesFilterPinned,
                                                limit=100)
    if not isinstance(pinned_messages, list):
        raise ValueError('pinned_messages is not a list')

    pinned_msg: Message
    for pinned_msg in pinned_messages:
        await client.unpin_message(bot._self_id, pinned_msg.id)

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
                        handlers=[StreamHandler(sys.stdout), BotLogHandler(msg), stream])
    logging.getLogger('telethon.client.updates').setLevel(logging.WARN)

    initiate_handlers()

    logging.info('Checking for updates...')

    update_log = await get_update_log()
    if update_log:
        me = await bot.get_me()
        if not isinstance(me, User):
            raise ValueError('me is not a User')

        logging.info('Update found, sending message')
        await bot.send_message(client._self_id,
                               f'Найдены обновления:\n\n'
                               f'<pre><code class="language-log">{update_log}</code></pre>\n'
                               'Введите /update для обновления')
    else:
        logging.info('No updates found')

    logging.info('Started successfully')
    await client.disconnected

    logging.info('Stopped')
    save_config()


if __name__ == '__main__':
    with client:
        try:
            client.loop.run_until_complete(main())
        except KeyboardInterrupt:
            logging.info('Stopping')
