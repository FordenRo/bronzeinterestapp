from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from handlers.read_handler import register_on_read_event

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if 'люблю' not in message.text:
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    for k in range(int(lifetime / 11.1)):
        try:
            text = message.text
            start = text.find('люблю')
            end = start + 5
            for i in range(5):
                l = list(text)
                word = list('люблю')
                word[i] = word[i].upper()
                l[start:end] = word
                await message.edit(''.join(l))
                await sleep(0.1)
            await message.edit(text)

            await sleep(5)

            for i in range(3):
                l = list(text)
                l[start:end] = ('❤️' if i % 2 == 0 else '💜️') * 3
                await message.edit(''.join(l))
                await sleep(0.2)

            await message.edit(text)
            await sleep(5)
        except MessageIdInvalidError:
            return
