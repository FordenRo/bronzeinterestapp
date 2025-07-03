from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client, cmd_block

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if cmd_block:
        return
    if '-_-' not in message.text:
        return

    client.loop.create_task(anim(message))


async def anim(message: Message):
    for i in range(int(lifetime / 5)):
        try:
            text = message.text
            await message.edit(text.replace('-_-', '=_='))
            await sleep(1)
            await message.edit(text)
            await sleep(4)
        except MessageIdInvalidError:
            return
