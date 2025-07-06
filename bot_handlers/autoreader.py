from asyncio import gather
import logging
import re

from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.types import User

from client import bot, client
from config import config, help_messages
from utils import get_user, user_to_link

current_state = False
tasks = {}

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
        await message.respond('Пользователь не найден')
        return

    config['auto_read'][str(user.id)] = {
        'silent': silent,
        'onetime': onetime
    }

    register_auto_read(user.id)
    await message.respond(
        f'Все сообщения от {user_to_link(user)} будут прочитаны {'тихо' if silent else 'и пересланы сюда'}{' один раз' if onetime else ''}')


def register_auto_read(id: int):
    autoread = config['auto_read'][str(id)]
    silent, onetime = autoread['silent'], autoread['onetime']

    @client.on(NewMessage([id], incoming=True))
    async def on_message(message: Message):
        await message.mark_read()
        if not silent:
            user = await get_user(id)
            if not isinstance(user, User):
                return

            if client._self_id is None:
                return

            await bot.send_message(client._self_id, f'Сообщение от {user_to_link(user)}: {message.text}')

        if onetime:
            client.remove_event_handler(on_message)
            tasks.pop(id)
            config['auto_read'].pop(str(id))

    tasks[id] = on_message
    logging.getLogger('autoreader').info(
        f'Registered user {id}{' (silent)' if silent else ''}{' (onetime)' if onetime else ''}')


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
        await message.respond('Пользователь не найден')
        return

    if str(user.id) in tasks:
        client.remove_event_handler(tasks[user.id])
        tasks.pop(user.id)
        config['auto_read'].pop(str(user.id))
    else:
        await message.respond('Пользователь не в списке авточитателя')
        return

    await message.respond(f'Авточитатель убран от {user_to_link(user)}')


@bot.on(NewMessage(incoming=True, pattern='autoreader list'))
async def autoreader_list(message: Message):
    user_list = await gather(*[get_user(int(i)) for i in config['auto_read']])
    name_list = [f'{user_to_link(user)}{' (тихий)' if config['auto_read'][str(user.id)]['silent'] else ''}{' (одноразовый)' if config['auto_read'][str(user.id)]['onetime'] else ''}'
                 for user in user_list if user is not None]
    await message.respond('Авточитатель:\n' + '\n'.join(name_list))


@bot.on(NewMessage(incoming=True, pattern='autoreader help'))
async def help(message: Message):
    await message.respond(help_messages['autoreader'])


[register_auto_read(int(i)) for i in config['auto_read']]
