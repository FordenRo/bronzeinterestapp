import sys
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE

from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import bot, client


@bot.on(NewMessage(incoming=True, pattern='stop'))
async def stop(message: Message):
    await message.respond('Stopping...')

    client.loop.stop()
    sys.exit()


@bot.on(NewMessage(incoming=True, pattern='restart'))
async def restart(message: Message):
    await message.respond('Restarting...')

    await create_subprocess_shell(f'"{sys.executable}" {' '.join(sys.argv)}')
    client.loop.stop()
    sys.exit()


@bot.on(NewMessage(incoming=True, pattern='update'))
async def update(message: Message):
    cmd = await create_subprocess_shell('git pull', stdout=PIPE)
    stdout, _ = await cmd.communicate()
    output = stdout.decode('utf8')

    if 'up to date' not in output:
        await message.respond(f'<pre>{output}</pre>')
        await restart(message)
    else:
        await message.respond('Already up to date')
