import re
from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from handlers.client.read_handler import register_on_read_event

chars = '.!)?'


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if not message.text or not re.search(f'[{chars}]' + '{2}', message.text):
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    if not message.text:
        return

    part = re.search(f'(?=[{chars}]' + '{2})' + f'[{chars}]+', message.text)
    if not part:
        return

    part = part.group()

    for _ in range(3):
        try:
            await sleep(3)
            eq = len(message.text) == len(part)
            for i in range(1 if eq else 0, len(part) + 1):
                await message.edit(message.text.replace(part, part[:i]))
                await sleep(0.2)
        except MessageIdInvalidError:
            return
