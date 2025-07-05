import re

from telethon.events import MessageRead, NewMessage, UserUpdate
from telethon.tl.custom import Message

from client import bot, client
from config import config
from utils import get_user, user_to_link

tasks = {'online': {}, 'read': {}}

if config.spy_list is None:
    config.spy_list = {'online': [], 'read': []}


@bot.on(NewMessage(incoming=True, pattern='spy (online|read) @[a-zA-Z0-9_]+ ?(onetime)?'))
async def command(message: Message):
    type, nickname, onetime = re.match('spy (online|read) (@[a-zA-Z0-9_]+) ?(onetime)?', message.text).groups()
    onetime = bool(onetime)
    user = await get_user(nickname)
    if not user:
        await message.respond('User not found')
        return

    if not onetime:
        config.spy_list[type] += [user.id]
    register_spy(type, user.id, onetime)
    await message.respond(f'{user_to_link(user)} will now spy {type}')


def register_spy(type: str, id: int, onetime: bool):
    if type == 'online':
        @client.on(UserUpdate([id]))
        async def on_update(event: UserUpdate.Event):
            if event.online:
                await bot.send_message((await client.get_me()).id, f'{user_to_link(await event.get_chat())} is online!')
                if onetime:
                    client.remove_event_handler(on_update)

        if not onetime:
            tasks['online'][id] = on_update
    elif type == 'read':
        @client.on(MessageRead([id]))
        async def on_read(event: MessageRead.Event):
            await bot.send_message((await client.get_me()).id,
                                   f'{user_to_link(await event.get_chat())} has read your messages!')
            if onetime:
                client.remove_event_handler(on_update)

        if not onetime:
            tasks['read'][id] = on_read


@bot.on(NewMessage(incoming=True, pattern='spy remove (online|read) @[a-zA-Z0-9_]+'))
async def remove(message: Message):
    type, nickname = re.match('spy remove (online|read) (@[a-zA-Z0-9_]+)', message.text).groups()
    user = await get_user(nickname)

    if user.id in config.spy_list[type]:
        config.spy_list[type].remove(user.id)
        client.remove_event_handler(tasks[type][user.id])
        await message.respond(f'{user_to_link(user)} removed from spy')
    else:
        await message.respond('User not found')


@bot.on(NewMessage(incoming=True, pattern='spy list'))
async def spy_list(message: Message):
    online_list = [user_to_link(await get_user(i)) for i in config.spy_list['online']]
    read_list = [user_to_link(await get_user(i)) for i in config.spy_list['read']]
    await message.respond('Online:\n' + '\n'.join(online_list) + '\n\nRead:\n' + '\n'.join(read_list))


@bot.on(NewMessage(incoming=True, pattern='spy help'))
async def spy_help(message: Message):
    await message.respond('\n'.join(['spy online|read @username onetime? - register spy',
                                     'spy remove online|read @username - remove from spy',
                                     'spy list - spy user list',
                                     'spy help - this message']))


for v in config.spy_list:
    for id in config.spy_list[v]:
        register_spy(v, id)
