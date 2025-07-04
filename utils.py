from logging import Handler

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


class LogHandler(Handler):
    def handle(self, record):
        print(record.getMessage())
        print(record.exc_text)
