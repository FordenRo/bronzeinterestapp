from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client

lifetime = 60


@client.on(NewMessage(outgoing=True, pattern='^❤️$'))
async def command(message: Message):
    for i in range(int(lifetime / 3)):
        await sleep(3)
        try:
            await message.edit('💜️' if i % 2 == 0 else '❤️')
        except MessageIdInvalidError:
            return
