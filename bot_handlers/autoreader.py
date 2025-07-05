from asyncio import gather
import logging
import re

from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.types import User

from client import bot, client
from config import config
from utils import get_user, user_to_link

current_state = False
tasks = {}
onetime_tasks = {}

if 'auto_read' not in config:
    config['auto_read'] = {}


@bot.on(NewMessage(incoming=True, pattern='autoreader @[a-zA-Z0-9_]+ ?(silent)? ?(onetime)?'))
async def command(message: Message):
    if not message.text:
        return

    match = re.match(
        'autoreader (@[a-zA-Z0-9_]+) ?(silent)? ?(onetime)?', message.text)
    if not match:
        return

    nickname, silent, onetime = match.groups()
    silent = bool(silent)
    onetime = bool(onetime)
    user = await get_user(nickname)
    if not user:
        await message.respond('User not found')
        return

    if not onetime:
        config['auto_read'][str(user.id)] = silent

    register_auto_read(user.id, silent, onetime)
    await message.respond(
        f'All messages from {user_to_link(user)} will be read {'silent' if silent else 'and forwarded here'}')


def register_auto_read(id: int, silent: bool, onetime: bool = False):
    @client.on(NewMessage([id], incoming=True))
    async def on_message(message: Message):
        await message.mark_read()
        if not silent:
            user = await get_user(id)
            if not isinstance(user, User):
                return

            if client._self_id is None:
                return

            await bot.send_message(client._self_id, f'Message from {user_to_link(user)}: {message.text}')

        if onetime:
            client.remove_event_handler(on_message)

    logging.getLogger('autoreader').info(f'Registered user {id}')
    if not onetime:
        tasks[id] = on_message


@bot.on(NewMessage(incoming=True, pattern='autoreader remove @[a-zA-Z0-9_]+'))
async def autoreader_remove(message: Message):
    if not message.text:
        return

    match = re.match('autoreader remove (@[a-zA-Z0-9_]+)', message.text)
    if not match:
        return

    nickname = match.group(1)
    user = await get_user(nickname)
    if not isinstance(user, User):
        await message.respond('User not found')
        return

    if str(user.id) in onetime_tasks:
        client.remove_event_handler(onetime_tasks[user.id])
        onetime_tasks.pop(user.id)
    elif str(user.id) in tasks:
        client.remove_event_handler(tasks[user.id])
        tasks.pop(user.id)
        config['auto_read'].pop(str(user.id))
    else:
        await message.respond('User not in autoreader list')
        return

    await message.respond(f'Autoreader removed from {user_to_link(user)}')


@bot.on(NewMessage(incoming=True, pattern='autoreader list'))
async def autoreader_list(message: Message):
    user_list = await gather(*[get_user(int(i)) for i in config['auto_read']])
    user_list += await gather(*[get_user(int(i)) for i in onetime_tasks])
    name_list = [f'{user_to_link(user)}{"silent" if config["auto_read"][str(user.id)] else ""}'
                 for user in user_list if user is not None]
    await message.respond('Autoreader:\n' + '\n'.join(name_list))


@bot.on(NewMessage(incoming=True, pattern='autoreader help'))
async def help(message: Message):
    await message.respond('\n'.join(['autoreader @nickname silent? onetime? - automaticaly read messages from user',
                                     'autoreader remove @nickname - remove autoreader from user',
                                     'autoreader list - autoreader user list',
                                     'autoreader help - this message']))


[register_auto_read(int(i), config['auto_read'][i])
 for i in config['auto_read']]
