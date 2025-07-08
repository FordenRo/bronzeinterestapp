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
    if not message.text or '-_-' not in message.text:
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    if not message.text:
        return

    for _ in range(int(lifetime / 5)):
        try:
            await message.edit(message.text.replace('-_-', '=_='))
            await sleep(1)
            await message.edit(message.text)
            await sleep(4)
        except MessageIdInvalidError:
            return
