from asyncio import gather
import logging
import re

from telethon.events import MessageRead, NewMessage, UserUpdate
from telethon.tl.custom import Message
from telethon.tl.types import User

from client import bot, client
from config import config, help_messages
from utils import get_user, user_to_link

tasks = {'online': {}, 'read': {}}

if 'spy_list' not in config:
    config['spy_list'] = {'online': {}, 'read': {}}


@bot.on(NewMessage(incoming=True, pattern='spy (online|read) @[a-zA-Z0-9_]+ ?(onetime)?'))
async def command(message: Message):
    if not message.text:
        return

    match = re.match(
        'spy (online|read) (@[a-zA-Z0-9_]+) ?(onetime)?', message.text)
    if not match:
        return

    type, nickname, onetime = match.groups()
    onetime = bool(onetime)
    user = await get_user(nickname)
    if not isinstance(user, User):
        await message.respond('Пользователь не найден')
        return

    config['spy_list'][type][user.id] = onetime
    register_spy(type, user.id)
    await message.respond(f'Следим за {'онлайном' if type == 'online' else 'чтением'} {user_to_link(user)}{' один раз' if onetime else ''}')


def register_spy(type: str, id: int):
    onetime = config['spy_list'][type][id]

    if type == 'online':
        @client.on(UserUpdate([id]))
        async def on_update(event: UserUpdate.Event):
            if event.online:
                if client._self_id is None:
                    return

                chat = await event.get_chat()
                if not isinstance(chat, User):
                    return

                await bot.send_message(client._self_id, f'{user_to_link(chat)} в сети!')
                if onetime:
                    client.remove_event_handler(on_update)
                    tasks['online'].pop(id)
                    config['spy_list'][type].pop(id)

        tasks['online'][id] = on_update
    elif type == 'read':
        @client.on(MessageRead([id]))
        async def on_read(event: MessageRead.Event):
            if client._self_id is None:
                return

            chat = await event.get_chat()
            if not isinstance(chat, User):
                return

            await bot.send_message(client._self_id, f'{user_to_link(chat)} прочитал ваши сообщения!')
            if onetime:
                client.remove_event_handler(on_update)
                tasks['read'].pop(id)
                config['spy_list'][type].pop(id)

        tasks['read'][id] = on_read

    logging.getLogger('spy').info(
        f'Registered spy {type} on user {id}{' (onetime)' if onetime else ''}')


@bot.on(NewMessage(incoming=True, pattern='spy remove (online|read) @[a-zA-Z0-9_]+'))
async def remove(message: Message):
    if not message.text:
        return

    match = re.match('spy remove (online|read) (@[a-zA-Z0-9_]+)', message.text)
    if not match:
        return

    type, nickname = match.groups()
    user = await get_user(nickname)
    if not isinstance(user, User):
        await message.respond('Пользователь не найден')
        return

    if str(user.id) in tasks[type]:
        client.remove_event_handler(tasks[type][user.id])
        tasks[type].pop(user.id)
        config['spy_list'][type].pop(user.id)
    else:
        await message.respond('Пользователь не в списке слежения')
        return

    await message.respond(f'{user_to_link(user)} убран из слежения')


@bot.on(NewMessage(incoming=True, pattern='spy list'))
async def spy_list(message: Message):
    online_list = await gather(*[get_user(i) for i in config['spy_list']['online']])
    read_list = await gather(*[get_user(i) for i in config['spy_list']['read']])
    online_list = [f'{user_to_link(user)}{' (одноразовый)' if config['spy_list']['online'][user.id] else ''}'
                   for user in online_list if user is not None]
    read_list = [f'{user_to_link(user)}{' (одноразовый)' if config['spy_list']['read'][user.id] else ''}'
                 for user in read_list if user is not None]
    await message.respond('Онлайн:\n' + '\n'.join(online_list) + '\n\nЧтение:\n' + '\n'.join(read_list))


@bot.on(NewMessage(incoming=True, pattern='spy help'))
async def spy_help(message: Message):
    await message.respond(help_messages['spy'])


[register_spy(v, int(id)) for v in config['spy_list']
 for id in config['spy_list'][v]]
