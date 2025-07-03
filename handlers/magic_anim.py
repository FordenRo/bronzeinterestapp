from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if 'магия' not in message.text:
        return

    for i in range(int(lifetime / 6)):
        try:
            text = message.text
            await message.edit(text.replace('магия', '<s>magic</s>'), parse_mode='html')
            await sleep(3)
            await message.edit(text)
            await sleep(3)
        except MessageIdInvalidError:
            return
