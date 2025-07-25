import sys
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE

from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import bot, client
from config import help_messages
from utils import NewMessageEvent


@bot.on(NewMessage(incoming=True, pattern=r'/stop'))
async def stop(message: NewMessageEvent):
    await message.respond('Останавливаю...')

    client.loop.stop()
    sys.exit()


@bot.on(NewMessage(incoming=True, pattern=r'/restart'))
async def restart(message: NewMessageEvent):
    await message.respond('Перезапускаю...')

    await create_subprocess_shell(f'"{sys.executable}" {' '.join(sys.argv)}')
    client.loop.stop()
    sys.exit()


async def get_update_log():
    await (await create_subprocess_shell('git fetch', stdout=PIPE)).communicate()
    cmd = await create_subprocess_shell('git log --oneline master..origin', stdout=PIPE)
    stdout, _ = await cmd.communicate()
    return stdout.decode('utf8')


async def pull():
    cmd = await create_subprocess_shell('git pull', stdout=PIPE)
    stdout, _ = await cmd.communicate()
    return stdout.decode('utf8')


@bot.on(NewMessage(incoming=True, pattern=r'/update'))
async def update(message: NewMessageEvent):
    has_update = await update_check(message)

    if has_update:
        await message.respond('Применяю обновления...')
        output = await pull()
        await message.respond(f'<pre><code class="language-log">{output}</code></pre>')
        await restart(message)


@bot.on(NewMessage(incoming=True, pattern=r'/check_updates'))
async def update_check(message: NewMessageEvent):
    responce = await message.respond('Проверяю обновления...')
    if not isinstance(responce, Message):
        return

    output = await get_update_log()

    if output:
        await responce.edit(
            f'Найдены обновления:\n\n'
            f'<pre><code class="language-log">{output}</code></pre>')
        return True
    else:
        await responce.edit('Обновление не требуется')


@bot.on(NewMessage(incoming=True, pattern=r'/help'))
async def help_command(message: NewMessageEvent):
    help_text = [
        '<b>Системные команды:</b>',
        help_messages['system'],
        '',
        '<b>Слежение:</b>',
        help_messages['spy'],
        '',
        '<b>Автоответчик:</b>',
        help_messages['autoresponder'],
        '',
        '<b>Авточитатель:</b>',
        help_messages['autoreader'],
        '',
        '<b>Всегда онлайн:</b>',
        help_messages['online'],
        '',
        '<b>Логи:</b>',
        help_messages['log'],
        '',
        '<code>help</code> - <i>показать эту справку</i>'
    ]
    await message.respond('\n'.join(help_text))
