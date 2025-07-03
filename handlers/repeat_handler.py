import re

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client, cmd_block, set_cmd_block

lifetime = 60


@client.on(NewMessage(outgoing=True, pattern='.r\\d+ .*'))
async def command(message: Message):
    if cmd_block:
        return

    client.loop.create_task(repeat(message))


async def repeat(message: Message):
    try:
        set_cmd_block(True)

        text = message.text
        count, msg = re.match('.r(\\d+) (.*)', text).groups()
        client.loop.create_task(message.delete())
        tasks = []
        for i in range(int(count)):
            tasks += [client.loop.create_task(message.respond(msg))]
    except MessageIdInvalidError:
        return
