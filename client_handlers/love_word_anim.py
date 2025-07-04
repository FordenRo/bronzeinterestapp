import re
from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from client_handlers.read_handler import register_on_read_event

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if not re.search('люблю', message.text, re.IGNORECASE):
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    for k in range(int(lifetime / 11.1)):
        try:
            part = re.search('люблю', message.text, re.IGNORECASE).group()
            for i in range(5):
                word = list(part)
                word[i] = word[i].upper() if word[i].islower() else word[i].lower()
                await message.edit(message.text.replace(part, ''.join(word)))
                await sleep(0.1)
            await message.edit(message.text)

            await sleep(5)

            for i in range(3):
                await message.edit(message.text.replace(part, ('❤️' if i % 2 == 0 else '💜️') * 3))
                await sleep(0.2)

            await message.edit(message.text)
            await sleep(5)
        except MessageIdInvalidError:
            return
