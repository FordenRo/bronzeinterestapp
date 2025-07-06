from asyncio import gather
import logging
import re

from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.types import User

from client import bot, client
from config import config, help_messages
from utils import get_user, user_to_link

if 'auto_respond' not in config:
    config['auto_respond'] = {}

tasks = {}
onetime_tasks = {}


@bot.on(NewMessage(incoming=True, pattern='autoresponder @[a-zA-Z0-9_]+ ?(silent)? ?(onetime)? .*'))
async def command(message: Message):
    if not message.text:
        return

    match = re.match(
        'autoresponder (@[a-zA-Z0-9]+) ?(silent)? ?(onetime)? (.*)', message.text)
    if not match:
        return

    nickname, silent, onetime, text = match.groups()
    onetime = bool(onetime)
    user = await get_user(nickname)
    if not isinstance(user, User):
        await message.respond('Пользователь не найден')
        return

    register_respond(user.id, text, bool(silent), onetime)
    await message.respond(f'Сообщения от {user_to_link(user)} будут отвечены введеным текстом {'тихо' if silent else 'и пересланы сюда'}')


def register_respond(id: int, text: str, silent: bool, onetime: bool = False):
    @client.on(NewMessage([id], incoming=True))
    async def on_message(message: Message):
        await message.respond(text)
        if not silent:
            user = await get_user(id)
            if not isinstance(user, User):
                return

            if client._self_id is None:
                return

            await bot.send_message(client._self_id, f'Сообщение от {user_to_link(user)}: {message.text}')

        if onetime:
            client.remove_event_handler(on_message)
            onetime_tasks.pop(id)

    if onetime:
        onetime_tasks[id] = on_message
    else:
        tasks[id] = on_message

        config['auto_respond'][str(id)] = {
            'text': text,
            'silent': silent
        }

    logging.getLogger('autoresponder').info(
        f'Registered user {id} with text: {text}')


@bot.on(NewMessage(incoming=True, pattern='autoresponder remove @[a-zA-Z0-9_]+'))
async def autorespond_remove(message: Message):
    if not message.text:
        return

    match = re.match('autoresponder remove (@[a-zA-Z0-9_]+)', message.text)
    if not match:
        return

    nickname = match.group(1)
    user = await get_user(nickname)
    if not isinstance(user, User):
        await message.respond('Пользователь не найден')
        return

    if str(user.id) in onetime_tasks:
        client.remove_event_handler(onetime_tasks[user.id])
        onetime_tasks.pop(user.id)
    elif str(user.id) in tasks:
        client.remove_event_handler(tasks[user.id])
        tasks.pop(user.id)
        config['auto_respond'].pop(str(user.id))
    else:
        await message.respond('Пользователь не в списке автоответчика')
        return

    await message.respond(f'Автоответчик убран от {user_to_link(user)}')


@bot.on(NewMessage(incoming=True, pattern='autoresponder list'))
async def autorespond_list(message: Message):
    user_list = await gather(*[get_user(int(i)) for i in config['auto_respond']])
    user_list += await gather(*[get_user(int(i)) for i in onetime_tasks])
    name_list = [f'{user_to_link(user)}{"silent" if config["auto_respond"][str(user.id)]["silent"] else ""}'
                 for user in user_list if user is not None]
    await message.respond('Автоответчик:\n' + '\n'.join(name_list))


@bot.on(NewMessage(incoming=True, pattern='autoresponder help'))
async def autorespond_help(message: Message):
    await message.respond(help_messages['autoresponder'])


[register_respond(int(i), config['auto_respond'][i]['text'],
                  config['auto_respond'][i]['silent']) for i in config['auto_respond']]
