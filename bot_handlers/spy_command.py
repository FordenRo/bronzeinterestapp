import re

from telethon.events import MessageRead, NewMessage, UserUpdate
from telethon.tl.custom import Message
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User, UserEmpty

from client import bot, client
from config import config

if config.spy_list is None:
    config.spy_list = {'online': [], 'read': []}


async def get_user(id: str | int) -> UserEmpty | User:
    return (await client(GetFullUserRequest(id))).users[0]


@bot.on(NewMessage(incoming=True, pattern='spy (online|read) @[a-zA-Z0-9]+'))
async def command(message: Message):
    type, nickname = re.match('spy (online|read) (@[a-zA-Z0-9]+)', message.text).groups()
    user = await get_user(nickname)
    if not user:
        await message.respond('User not found')
        return

    config.spy_list[type] += [user.id]
    register_spy(type, user.id)
    await message.respond(f'{user.first_name} will now spy {type}')


def register_spy(type: str, id: int):
    if type == 'online':
        @client.on(UserUpdate([id]))
        async def on_update(event: UserUpdate.Event):
            if event.online:
                await bot.send_message((await client.get_me()).id, f'{(await event.get_chat()).first_name} is online!')
    elif type == 'read':
        @client.on(MessageRead([id]))
        async def on_read(event: MessageRead.Event):
            await bot.send_message((await client.get_me()).id,
                                   f'{(await event.get_chat()).first_name} has read your messages!')


@bot.on(NewMessage(incoming=True, pattern='spy remove (online|read) @[a-zA-Z0-9]+'))
async def remove(message: Message):
    type, nickname = re.match('spy remove (online|read) (@[a-zA-Z0-9]+)', message.text).groups()
    user = await get_user(nickname)
    if user.id in config.spy_list[type]:
        config.spy_list[type].remove(user.id)
        await message.respond(f'{user.first_name} removed from spy')
    else:
        await message.respond('User not found')


@bot.on(NewMessage(incoming=True, pattern='spy list'))
async def spy_list(message: Message):
    online_list = [(await get_user(i)).first_name for i in config.spy_list['online']]
    read_list = [(await get_user(i)).first_name for i in config.spy_list['read']]
    await message.respond('Online:\n' + '\n'.join(online_list) + '\n\nRead:\n' + '\n'.join(read_list))


@bot.on(NewMessage(incoming=True, pattern='spy help'))
async def spy_help(message: Message):
    await message.respond('\n'.join(['spy online|read @username - register spy',
                                     'spy remove online|read @username - remove from spy',
                                     'spy list - spy users list',
                                     'spy help - this message']))


for v in config.spy_list:
    for id in config.spy_list[v]:
        register_spy(v, id)
