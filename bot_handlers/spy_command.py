from asyncio import gather
import logging
import re

from telethon.events import MessageRead, NewMessage, UserUpdate
from telethon.tl.custom import Message
from telethon.tl.types import User

from client import bot, client
from config import config
from utils import get_user, user_to_link

tasks = {'online': {}, 'read': {}}

if 'spy_list' not in config:
    config['spy_list'] = {'online': [], 'read': []}


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
        await message.respond('User not found')
        return

    if not onetime:
        config['spy_list'][type] += [user.id]
    register_spy(type, user.id, onetime)
    await message.respond(f'{user_to_link(user)} will now spy {type}')


def register_spy(type: str, id: int, onetime: bool = False):
    if type == 'online':
        @client.on(UserUpdate([id]))
        async def on_update(event: UserUpdate.Event):
            if event.online:
                if client._self_id is None:
                    return

                chat = await event.get_chat()
                if not isinstance(chat, User):
                    return

                await bot.send_message(client._self_id, f'{user_to_link(chat)} is online!')
                if onetime:
                    client.remove_event_handler(on_update)

        if not onetime:
            tasks['online'][id] = on_update
    elif type == 'read':
        @client.on(MessageRead([id]))
        async def on_read(event: MessageRead.Event):
            if client._self_id is None:
                return

            chat = await event.get_chat()
            if not isinstance(chat, User):
                return

            await bot.send_message(client._self_id, f'{user_to_link(chat)} has read your messages!')
            if onetime:
                client.remove_event_handler(on_update)

        if not onetime:
            tasks['read'][id] = on_read
    logging.getLogger('spy').info(f'Registered spy {type} on user {id}')


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
        await message.respond('User not found')
        return

    if user.id in config['spy_list'][type]:
        config['spy_list'][type].remove(user.id)
        client.remove_event_handler(tasks[type][user.id])
        await message.respond(f'{user_to_link(user)} removed from spy')
    else:
        await message.respond('User not found')


@bot.on(NewMessage(incoming=True, pattern='spy list'))
async def spy_list(message: Message):
    online_list = await gather(*[get_user(i) for i in config['spy_list']['online']])
    read_list = await gather(*[get_user(i) for i in config['spy_list']['read']])
    online_list = [user_to_link(user)
                   for user in online_list if user is not None]
    read_list = [user_to_link(user) for user in read_list if user is not None]
    await message.respond('Online:\n' + '\n'.join(online_list) + '\n\nRead:\n' + '\n'.join(read_list))


@bot.on(NewMessage(incoming=True, pattern='spy help'))
async def spy_help(message: Message):
    await message.respond('\n'.join(['spy online|read @username onetime? - register spy',
                                     'spy remove online|read @username - remove from spy',
                                     'spy list - spy user list',
                                     'spy help - this message']))


[register_spy(v, id) for v in config['spy_list']
 for id in config['spy_list'][v]]
