from asyncio import sleep

from telethon.errors import MessageIdInvalidError
from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from client_handlers.read_handler import register_on_read_event

lifetime = 60


@client.on(NewMessage(outgoing=True))
async def command(message: Message):
    if not message.text or 'хочу' not in message.text or 'тебя' not in message.text:
        return

    register_on_read_event(message, anim)


async def anim(message: Message):
    if not message.text:
        return

    for _ in range(int(lifetime / 5.6)):
        try:
            await sleep(5)
            await message.edit(message.text.replace('хочу', 'want'))
            await sleep(0.2)
            await message.edit(message.text.replace('хочу', '<s>want</s>'))
            await sleep(0.2)
            await message.edit(message.text.replace('хочу', 'want'))
            await sleep(0.2)
            await message.edit(message.text)
        except MessageIdInvalidError:
            return
