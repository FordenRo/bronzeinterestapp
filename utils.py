from asyncio import sleep
from logging import Handler
import logging

from telethon.tl.custom import Message
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User, UserEmpty

from client import bot, client


def lerp(a, b, t):
    return a * (1 - t) + b * t


async def get_user(id: str | int) -> User | None:
    try:
        return (await client(GetFullUserRequest(id))).users[0]  # type: ignore
    except ValueError:
        return None


def user_to_link(user: User | UserEmpty):
    if isinstance(user, UserEmpty):
        return ''

    if user.username:
        link = f'tg://resolve?domain={user.username}'
    elif user.phone:
        link = f'tg://resolve?phone={user.phone}'
    else:
        link = f'tg://user?id={user.id}'

    return f'<a href="{link}">{user.first_name}{f' {user.last_name}' if user.last_name else ''}</a>'


class TgLogHandler(Handler):
    def __init__(self, message: Message):
        super().__init__()

        self.name = 'TelegramLog'
        self.message = message
        self.content = ''
        self._task = None

    def handle(self, record):
        if record.levelno >= logging.ERROR:
            if client._self_id is None:
                return

            client.loop.create_task(bot.send_message(
                client._self_id, f'<pre><code class="language-log">{self.format(record)}</code></pre>'))
            return

        self.content += self.format(record) + '\n'
        if self._task:
            return

        self._task = client.loop.create_task(self.update())

    async def update(self):
        await sleep(0.5)
        text = self.content
        if len(text) > 2048:
            text = text[-2048:]
            text = '\n'.join(text.splitlines()[1:])

        if self.message is None:
            return

        self._task = None
        await self.message.edit(f'<pre><code class="language-log">{'\n'.join(text.splitlines()[::-1])}</code></pre>')
