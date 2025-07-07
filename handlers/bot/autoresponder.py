from asyncio import gather
import logging

from telethon.events import NewMessage
from telethon.tl.types import User

from client import bot, client
from config import config, help_messages
from utils import NewMessageEvent, get_user, user_to_link

if 'auto_respond' not in config:
    config['auto_respond'] = {}

tasks = {}


@bot.on(NewMessage(incoming=True,
                   pattern=r'autoresponder @?([a-zA-Z0-9_]+) ?(silent)? ?(onetime)? (.+)'))
async def command(message: NewMessageEvent):
    if not message.text:
        return

    nickname, silent, onetime, text = message.pattern_match.groups()
    onetime = bool(onetime)
    silent = bool(silent)
    user = await get_user(nickname)
    if not isinstance(user, User):
        await message.respond('Пользователь не найден')
        return

    config['auto_respond'][str(user.id)] = {
        'text': text,
        'silent': silent,
        'onetime': onetime
    }

    register_respond(user.id)
    await message.respond(f'Сообщения от {user_to_link(user)} будут отвечены введеным текстом '
                          f'{'тихо' if silent else 'и пересланы сюда'}'
                          f'{' один раз' if onetime else ''}')


def register_respond(id: int):
    autorespond = config['auto_respond'][str(id)]
    text, silent, onetime = autorespond['text'], autorespond['silent'], autorespond['onetime']

    @client.on(NewMessage([id], incoming=True))
    async def on_message(message: NewMessageEvent):
        await message.respond(text)
        if not silent:
            user = await get_user(id)
            if not isinstance(user, User):
                return

            if client._self_id is None:
                return

            await bot.send_message(client._self_id,
                                   f'Сообщение от {user_to_link(user)}: {message.text}')

        if onetime:
            client.remove_event_handler(on_message)
            tasks.pop(id)
            config['auto_respond'].pop(str(id))

    config['auto_respond'][str(id)] = {
        'text': text,
        'silent': silent,
        'onetime': onetime
    }

    tasks[id] = on_message
    logging.getLogger('autoresponder').info(f'Registered user {id}{' (silent)' if silent else ''}'
                                            f'{' (onetime)' if onetime else ''} with text: {text}')


@bot.on(NewMessage(incoming=True, pattern=r'autoresponder remove @?([a-zA-Z0-9_]+)'))
async def autorespond_remove(message: NewMessageEvent):
    if not message.text:
        return

    nickname = message.pattern_match.group(1)
    user = await get_user(nickname)
    if not isinstance(user, User):
        await message.respond('Пользователь не найден')
        return

    if user.id in tasks:
        client.remove_event_handler(tasks[user.id])
        tasks.pop(user.id)
        config['auto_respond'].pop(str(user.id))
    else:
        await message.respond('Пользователь не в списке автоответчика')
        return

    await message.respond(f'Автоответчик убран от {user_to_link(user)}')


@bot.on(NewMessage(incoming=True, pattern=r'autoresponder list'))
async def autorespond_list(message: NewMessageEvent):
    user_list = await gather(*[get_user(int(i)) for i in config['auto_respond']])
    name_list = [f'{user_to_link(user)}'
                 f'{' (тихий)' if config['auto_respond'][str(user.id)]['silent'] else ''}'
                 f'{' (одноразовый)' if config['auto_respond'][str(user.id)]['onetime'] else ''} '
                 f'- {config['auto_respond'][str(user.id)]['text']}'
                 for user in user_list if user is not None]
    await message.respond('Автоответчик:\n' + '\n'.join(name_list))


@bot.on(NewMessage(incoming=True, pattern=r'autoresponder help'))
async def autorespond_help(message: NewMessageEvent):
    await message.respond(help_messages['autoresponder'])


[register_respond(int(i)) for i in config['auto_respond']]
