import logging
from io import BytesIO, StringIO
from logging import StreamHandler

from telethon.events import NewMessage

from client import bot
from config import help_messages
from handlers.bot.log_handler import BotLogHandler
from utils import NewMessageEvent


@bot.on(NewMessage(incoming=True, pattern=r'log send'))
async def send_log(message: NewMessageEvent):
    log = logging.getHandlerByName('Stream')
    if not isinstance(log, StreamHandler):
        return

    stream: StringIO = log.stream

    io = BytesIO(stream.getvalue().encode('utf8'))
    io.name = 'interest.log'

    if message.chat_id is None:
        return

    await bot.send_file(message.chat_id, io)


@bot.on(NewMessage(incoming=True, pattern=r'log (clear|cls)'))
async def log_clear(message: NewMessageEvent):
    log = logging.getHandlerByName('TelegramLog')
    if not isinstance(log, BotLogHandler):
        return

    log.content = ''
    logging.getLogger('log').info('Cleared')

    await message.respond('Лог очищен')


@bot.on(NewMessage(incoming=True, pattern=r'log help'))
async def log_help(message: NewMessageEvent):
    await message.respond(help_messages['log'])
