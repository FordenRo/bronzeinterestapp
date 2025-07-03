import re
from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client

lifetime = 60


@client.on(NewMessage(outgoing=True, pattern='.r\\d+ .*'))
async def command(message: Message):
    try:
        text = message.text
        count, msg = re.match('.r(\\d+) (.*)', text).groups()
        client.loop.create_task(message.delete())
        for i in range(int(count)):
            client.loop.create_task(message.respond(msg))
    except MessageIdInvalidError:
        return
