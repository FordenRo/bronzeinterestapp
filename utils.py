from asyncio import sleep
from logging import Handler

from telethon.tl.custom import Message
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User, UserEmpty

from client import client


def lerp(a, b, t):
    return a * (1 - t) + b * t


async def get_user(id: str | int) -> UserEmpty | User:
    return (await client(GetFullUserRequest(id))).users[0]


def user_to_link(user: User | UserEmpty):
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

        self.message = message
        self.content = ''
        self._task = None

    def handle(self, record):
        self.content += self.format(record) + '\n'
        if self._task:
            return

        self._task = client.loop.create_task(self.update())

    async def update(self):
        await sleep(0.5)
        await self.message.edit(f'<pre>{self.content}</pre>', parse_mode='html')
        self._task = None
