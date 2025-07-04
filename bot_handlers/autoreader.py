import re

from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import bot, client
from config import config
from utils import get_user, user_to_link

current_state = False
tasks = {}

if config.auto_read is None:
    config.auto_read = {}


@bot.on(NewMessage(incoming=True, pattern='autoreader @[a-zA-Z0-9_]+ ?(silent)?'))
async def command(message: Message):
    nickname, silent = re.match('autoreader (@[a-zA-Z0-9_]+) ?(silent)?', message.text).groups()
    silent = bool(silent)
    user = await get_user(nickname)
    if not user:
        await message.respond('User not found')
        return

    config.auto_read[user.id] = silent
    register_auto_read(user.id, silent)
    await message.respond(
        f'All messages from {user_to_link(user)} will be read {'silent' if silent else 'and forwarded here'}',
        parse_mode='html')


def register_auto_read(id: int, silent: bool):
    @client.on(NewMessage([id], incoming=True))
    async def on_message(message: Message):
        nonlocal silent

        await message.mark_read()
        if not silent:
            user = await get_user(id)
            await bot.send_message((await client.get_me()).id, f'Message from {user_to_link(user)}: {message.text}',
                                   parse_mode='html')

    tasks[id] = on_message


@bot.on(NewMessage(incoming=True, pattern='autoreader remove @[a-zA-Z0-9_]+'))
async def autoreader_remove(message: Message):
    nickname = re.match('autoreader (@[a-zA-Z0-9_]+)', message.text).group(1)
    user = await get_user(nickname)

    if user.id in config.auto_read:
        config.auto_read.pop(nickname)
        client.remove_event_handler(tasks[user.id])
        await message.respond(f'Autoreader removed from {user_to_link(user)}', parse_mode='html')
    else:
        await message.respond('User not found')


@bot.on(NewMessage(incoming=True, pattern='autoreader list'))
async def autoreader_list(message: Message):
    user_list = [f'{user_to_link(await get_user(int(i)))}{' silent' if config.auto_read[i] else ''}' for i in
                 config.auto_read]
    await message.respond('Autoreader:\n' + '\n'.join(user_list), parse_mode='html')


@bot.on(NewMessage(incoming=True, pattern='autoreader help'))
async def help(message: Message):
    await message.respond('\n'.join(['autoreader @nickname silent? - automaticaly read messages from user',
                                     'autoreader remove @nickname - remove autoreader from user',
                                     'autoreader list - autoreader user list',
                                     'autoreader help - this message']))


for i in config.auto_read:
    silent = config.auto_read[i]
    register_auto_read(int(i), silent)
