from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if '❤️' not in message.text:
        return

    client.loop.create_task(anim(message))


async def anim(message: Message):
    for i in range(int(lifetime / 6)):
        try:
            text = message.text
            await sleep(3)
            await message.edit(text.replace('❤️', '💜️'))
            await sleep(3)
            await message.edit(text)
        except MessageIdInvalidError:
            return
