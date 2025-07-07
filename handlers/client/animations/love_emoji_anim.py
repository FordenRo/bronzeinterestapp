from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from handlers.client.read_handler import register_on_read_event
from utils import NewMessageEvent

lifetime = 60
emojis = ['💜️', '🩷', '💛', '💙', '💚']


@client.on(NewMessage(outgoing=True))
async def command(message: NewMessageEvent):
    if not message.text or '❤️' not in message.text:
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    if not message.text:
        return

    for i in range(int(lifetime / (3 + len(emojis) * 3))):
        try:
            text = message.text
            await sleep(3)
            for i in emojis:
                await message.edit(text.replace('❤️', i))
                await sleep(3)
            await message.edit(text)
        except MessageIdInvalidError:
            return
