import logging
from io import BytesIO, StringIO
from logging import StreamHandler

from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import bot
from utils import TgLogHandler


@bot.on(NewMessage(incoming=True, pattern='log send'))
async def send_log(message: Message):
    log = logging.getHandlerByName('Stream')
    if not isinstance(log, StreamHandler):
        return

    stream: StringIO = log.stream

    io = BytesIO(stream.getvalue().encode('utf8'))
    io.name = 'interest.log'

    if message.chat_id is None:
        return

    await bot.send_file(message.chat_id, io)


@bot.on(NewMessage(incoming=True, pattern='log (clear|cls)'))
async def log_clear(message: Message):
    log = logging.getHandlerByName('TelegramLog')
    if not isinstance(log, TgLogHandler):
        return

    log.content = ''
    logging.getLogger('log').info('Cleared')

    await message.respond('Log cleared')


@bot.on(NewMessage(incoming=True, pattern='log help'))
async def log_help(message: Message):
    await message.respond('\n'.join(['log send - send file with log',
                                     'log clear|cls - clear log message',
                                     'log help - this message']))
