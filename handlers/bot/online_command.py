from telethon.events import NewMessage, UserUpdate
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import UserStatusOnline

from client import bot, client
from config import help_messages
from utils import NewMessageEvent

current_state = False
online_task = None


@bot.on(NewMessage(incoming=True, pattern=r'(be|no) online'))
async def online(message: NewMessageEvent):
    global current_state, online_task

    if not message.text:
        return

    state = message.pattern_match.group(1) == 'be'
    if state != current_state:
        current_state = state
        await message.respond('Теперь вы будете всегда в онлайне' if state
                              else 'Постоянный онлайн выключен')
        if state:
            online_task = await always_online_handler()
        elif online_task:
            client.remove_event_handler(online_task)
    else:
        await message.respond('Ничего не изменилось')


async def always_online_handler():
    if client._self_id is None:
        return

    await client(UpdateStatusRequest(offline=False))

    @client.on(UserUpdate([client._self_id]))
    async def update(event: UserUpdate.Event):
        if event.status is not UserStatusOnline:
            await client(UpdateStatusRequest(offline=False))

    return update


@bot.on(NewMessage(incoming=True, pattern=r'online (state|status)'))
async def online_state(message: NewMessageEvent):
    await message.respond(f'Постоянный онлайн {'включен' if current_state else 'выключен'}')


@bot.on(NewMessage(incoming=True, pattern=r'online help'))
async def online_help(message: NewMessageEvent):
    await message.respond(help_messages['online'])
