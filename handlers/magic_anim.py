from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client

lifetime = 60


@client.on(NewMessage(outgoing=True, pattern='магия'))
async def command(message: Message):
    for i in range(int(lifetime / 6)):
        try:
            text = message.text
            await message.edit(text.replace('магия', 'magic'))
            await sleep(3)
            await message.edit(text)
            await sleep(3)
        except MessageIdInvalidError:
            return
