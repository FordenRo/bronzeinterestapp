import logging
import re

from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.types import User

from client import bot, client
from utils import get_user, user_to_link


@bot.on(NewMessage(incoming=True, pattern='autoresponder @[a-zA-Z0-9_]+ ?(silent)? .*'))
async def command(message: Message):
    if not message.text:
        return

    match = re.match(
        'autoresponder (@[a-zA-Z0-9]+) ?(silent)? (.*)', message.text)
    if not match:
        return

    nickname, silent, text = match.groups()
    user = await get_user(nickname)
    if not isinstance(user, User):
        await message.respond('User not found')
        return

    register_respond(user.id, text, bool(silent))
    await message.respond(f'Message from {user_to_link(user)} will be responded with text {'silent' if silent else 'and forwarded here'}')


def register_respond(id: int, text: str, silent: bool):
    @client.on(NewMessage([id], incoming=True))
    async def on_message(message: Message):
        await message.respond(text)
        if not silent:
            user = await get_user(id)
            if not isinstance(user, User):
                return

            if client._self_id is None:
                return

            await bot.send_message(client._self_id, f'Message from {user_to_link(user)}: {message.text}')

        client.remove_event_handler(on_message)
    logging.getLogger('autoresponder').info(
        f'Registered user {id} with text: {text}')


@bot.on(NewMessage(incoming=True, pattern='autoresponder help'))
async def autorespond_help(message: Message):
    await message.respond('\n'.join(['autoresponder @nickname silent? text - register autoresponder',
                                     'autoresponder help - this message']))
