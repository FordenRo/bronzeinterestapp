import re
from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from handlers.client.read_handler import register_on_read_event
from utils import NewMessageEvent

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: NewMessageEvent):
    if not message.text or not re.search(r'хочу тебя', message.text, re.IGNORECASE):
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    if not message.text:
        return

    part = re.search(r'хочу тебя', message.text, re.IGNORECASE)
    if not part:
        return

    part = part.group()
    for _ in range(int(lifetime / 5.6)):
        try:
            await sleep(5)

            for i in range(3):
                await message.edit(
                    message.text.replace(part, 'want' if i % 2 == 0 else '<s>want</s>'))
                await sleep(0.2)

            await message.edit(message.text)
        except MessageIdInvalidError:
            return
