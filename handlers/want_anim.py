from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if 'хочу' not in message.text:
        return

    for i in range(int(lifetime / 7)):
        try:
            await sleep(5)
            text = message.text
            await message.edit(text.replace('хочу', '||хочу||'))
            await sleep(1)
            await message.edit(text)
            await sleep(2)
            await message.edit(text.replace('~хочу~'))
        except MessageIdInvalidError:
            return
