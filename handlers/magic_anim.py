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
    if 'магия' not in message.text:
        return

    client.loop.create_task(anim(message))


async def anim(message: Message):
    for i in range(int(lifetime / 6)):
        try:
            text = message.text
            await message.edit(text.replace('магия', '<s>magic</s>'), parse_mode='html')
            await sleep(3)
            await message.edit(text)
            await sleep(3)
        except MessageIdInvalidError:
            return
