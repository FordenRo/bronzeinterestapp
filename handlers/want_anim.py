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
    if 'хочу' not in message.text:
        return
    if 'тебя' not in message.text:
        return

    client.loop.create_task(anim(message))


async def anim(message: Message):
    for i in range(int(lifetime / 5.6)):
        try:
            await sleep(5)
            text = message.text

            await message.edit(text.replace('хочу', 'want'), parse_mode='html')
            await sleep(0.2)
            await message.edit(text.replace('хочу', '<s>want</s>'), parse_mode='html')
            await sleep(0.2)
            await message.edit(text.replace('хочу', 'want'), parse_mode='html')
            await sleep(0.2)
            await message.edit(text)
        except MessageIdInvalidError:
            return
