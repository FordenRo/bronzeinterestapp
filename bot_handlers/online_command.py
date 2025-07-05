import re

from telethon.events import NewMessage, UserUpdate
from telethon.tl.custom import Message
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import UserStatusOnline

from client import bot, client

current_state = False
online_task = None


@bot.on(NewMessage(incoming=True, pattern='(be|no) online'))
async def online(message: Message):
    global current_state, online_task

    if not message.text:
        return

    match = re.match('(be|no) online', message.text)
    if not match:
        return

    state = match.group(1) == 'be'
    if state != current_state:
        current_state = state
        await message.respond('Now you will be online' if state else 'Always online turned off')
        if state:
            online_task = await always_online_handler()
        elif online_task:
            client.remove_event_handler(online_task)
    else:
        await message.respond('Nothing changed')


async def always_online_handler():
    if client._self_id is None:
        return

    await client(UpdateStatusRequest(offline=False))

    @client.on(UserUpdate([client._self_id]))
    async def update(event: UserUpdate.Event):
        if event.status is not UserStatusOnline:
            await client(UpdateStatusRequest(offline=False))

    return update


@bot.on(NewMessage(incoming=True, pattern='online (state|status)'))
async def online_state(message: Message):
    await message.respond(f'Always online is {'on' if current_state else 'off'}')


@bot.on(NewMessage(incoming=True, pattern='online help'))
async def online_help(message: Message):
    await message.respond('\n'.join(['be|no online - turn on|off always online',
                                     'online state|status - is always online active'
                                     'online help - this message']))
