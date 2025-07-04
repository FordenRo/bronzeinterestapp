from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from handlers.read_handler import register_on_read_event

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    register_on_read_event(message, anim)


async def anim(message: Message):
    chars = ['...', '!!!', '???', ')))']
    for i in chars:
        if i in message.text:
            l = i[0]
            break
    else:
        return

    for i in range(int(lifetime / 3.6)):
        try:
            text = message.text
            start = 0
            if len(text) == 3:
                start = 1
            for i in range(start, 3):
                await message.edit(text.replace(l * 3, l * i))
                await sleep(0.2)
            await message.edit(text)
            await sleep(3)
        except MessageIdInvalidError:
            return
