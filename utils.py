from re import Match

from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import User, UserEmpty

from client import client


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


class NewMessageEvent(NewMessage.Event, Message):
    pattern_match: Match
