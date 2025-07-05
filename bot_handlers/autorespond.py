import re

from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import bot, client
from utils import get_user, user_to_link


@bot.on(NewMessage(incoming=True, pattern='autorespond @[a-zA-Z0-9_]+ ?(silent)? .*'))
async def command(message: Message):
    nickname, silent, text = re.match('autorespond (@[a-zA-Z0-9]+) ?(silent)? (.*)', message.text).groups()
    user = await get_user(nickname)
    silent = bool(silent)
    if not user:
        await message.respond('User not found')

    register_respond(user.id, text, silent)
    await message.respond(f'Message from {user_to_link(user)} will be responded with text {'silent' if silent else 'and forwarded here'}')


def register_respond(id: int, text: str, silent: bool):
    @client.on(NewMessage([id], incoming=True))
    async def on_message(message: Message):
        await message.respond(text)
        if not silent:
            user = await get_user(id)
            await bot.send_message((await client.get_me()).id, f'Message from {user_to_link(user)}: {message.text}')

        client.remove_event_handler(on_message)


@bot.on(NewMessage(incoming=True, pattern='autorespond help'))
async def autorespond_help(message: Message):
    await message.respond('\n'.join(['autorespond @nickname silent? text - register autorespond',
                                     'autorespond help - this message']))
