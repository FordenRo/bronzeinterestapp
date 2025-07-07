from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage

from client import client
from utils import NewMessageEvent

lifetime = 60


@client.on(NewMessage(outgoing=True, pattern=r'.r(\d+) (.*)'))
async def command(message: NewMessageEvent):
    client.loop.create_task(repeat(message))


async def repeat(message: NewMessageEvent):
    if not message.text:
        return

    try:
        count, msg = message.pattern_match.groups()
        client.loop.create_task(message.delete())
        tasks = []
        for _ in range(int(count)):
            tasks += [client.loop.create_task(message.respond(msg))]
    except MessageIdInvalidError:
        return
