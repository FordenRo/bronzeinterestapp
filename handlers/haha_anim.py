import re
from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from handlers.read_handler import register_on_read_event


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if not re.search('(?=ха|ах)[ха]{5}', message.text, re.IGNORECASE):
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    part = re.search('(?=[ха]{5})(?=ха|ах)\\w+', message.text, re.IGNORECASE).group()
    for i in range(len(part) * (2 if len(part) < 15 else 1)):
        try:
            await sleep(0.4)
            p = i % len(part) + 1
            text = part[p:] + part[:p]
            await message.edit(message.text.replace(part, text))
        except MessageIdInvalidError:
            return
