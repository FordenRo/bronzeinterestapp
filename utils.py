from asyncio import sleep
from logging import Handler
import logging
from re import Match

from telethon.events import CallbackQuery, NewMessage
from telethon.tl.custom import Button, Message
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
        self.page = 0
        self._task = None

        bot.add_event_handler(self.page_callback,
                              CallbackQuery(pattern=r'log (\d+)'))

    def handle(self, record):
        if record.levelno >= logging.ERROR:
            if client._self_id is None:
                return

            client.loop.create_task(
                bot.send_message(
                    client._self_id,
                    f'<pre><code class="language-log">{self.format(record)}</code></pre>'))
            return

        self.content += self.format(record) + '\n'
        if self._task:
            return

        self._task = client.loop.create_task(self.update())

    async def page_callback(self, event: CallbackQuery):
        print(event.match)
        # self.page = int(event.pattern_match.group(1))
        # await self.update()

    async def update(self):
        await sleep(0.5)

        if self.message is None:
            return

        self._task = None

        buttons = [[Button.inline('Назад', f'log {self.page - 1}'),
                    Button.inline('Скачать', 'log download'),
                    Button.inline('Далее', f'log {self.page + 1}')]]

        await self.message.edit(
            '<pre><code class="language-log">'
            f'{'\n'.join(self.content.splitlines()[::-1][self.page * 100:(self.page + 1) * 100])}'
            '</code></pre>',
            buttons=buttons
        )


class NewMessageEvent(NewMessage.Event, Message):
    pattern_match: Match
