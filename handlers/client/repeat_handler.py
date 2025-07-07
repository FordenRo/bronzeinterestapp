import re

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client

lifetime = 60


@client.on(NewMessage(outgoing=True, pattern='.r\\d+ .*'))
async def command(message: Message):
    client.loop.create_task(repeat(message))


async def repeat(message: Message):
    if not message.text:
        return

    try:
        match = re.match('.r(\\d+) (.*)', message.text)
        if not match:
            return

        count, msg = match.groups()
        client.loop.create_task(message.delete())
        tasks = []
        for _ in range(int(count)):
            tasks += [client.loop.create_task(message.respond(msg))]
    except MessageIdInvalidError:
        return
