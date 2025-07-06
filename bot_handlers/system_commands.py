import sys
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE

from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import bot, client
from config import help_messages


@bot.on(NewMessage(incoming=True, pattern='stop'))
async def stop(message: Message):
    await message.respond('Останавливаю...')

    client.loop.stop()
    sys.exit()


@bot.on(NewMessage(incoming=True, pattern='restart'))
async def restart(message: Message):
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


@bot.on(NewMessage(incoming=True, pattern='update$'))
async def update(message: Message):
    update_log = await get_update_log()

    if update_log:
        output = await pull()
        await message.respond(f'<pre><code class="language-log">{update_log}\n{output}</code></pre>')
        await restart(message)
    else:
        await message.respond('Обновление не требуется')


@bot.on(NewMessage(incoming=True, pattern='update check'))
async def update_check(message: Message):
    output = await get_update_log()

    if output:
        await message.respond(f'<pre><code class="language-log">{output}</code></pre>')
    else:
        await message.respond('Обновление не требуется')


@bot.on(NewMessage(incoming=True, pattern='help'))
async def help_command(message: Message):
    help_text = [
        'Системные команды:',
        help_messages['system'],
        '',
        'Автоответчик:',
        help_messages['autoresponder'],
        '',
        'Авточитатель:',
        help_messages['autoreader'],
        '',
        'Онлайн статус:',
        help_messages['online'],
        '',
        'Логи:',
        help_messages['log'],
        '',
        'help - показать эту справку'
    ]
    await message.respond('\n'.join(help_text))
