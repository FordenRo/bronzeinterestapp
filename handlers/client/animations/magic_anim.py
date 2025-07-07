import re
from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from handlers.client.read_handler import register_on_read_event

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if not message.text or not re.search('магия', message.text, re.IGNORECASE):
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    if not message.text:
        return

    for _ in range(int(lifetime / 6)):
        try:
            part = re.search('магия', message.text, re.IGNORECASE)
            if not part:
                return

            part = part.group()
            await message.edit(message.text.replace(part, '<s>magic</s>'))
            await sleep(3)
            await message.edit(message.text)
            await sleep(3)
        except MessageIdInvalidError:
            return
