import logging

from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import bot, client
from utils import TgLogHandler


@bot.on(NewMessage(incoming=True, pattern='log send'))
async def send_log(message: Message):
    log: TgLogHandler | None = logging.getHandlerByName('TelegramLog')

    await bot.send_file(message.chat_id, log.content, caption='interest.log')


@bot.on(NewMessage(incoming=True, pattern='log (clear|cls)'))
async def log_clear(message: Message):
    log: TgLogHandler | None = logging.getHandlerByName('TelegramLog')
    log.content = ''
    logging.getLogger('log').info('Cleared')

    await message.respond('Log cleared')
