from asyncio import sleep
from logging import Handler
import logging
from re import Match

from telethon.events import CallbackQuery
from telethon.tl.custom import Button, Message

from client import bot, client


class BotLogHandler(Handler):
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

    async def page_callback(self, event: CallbackQuery.Event):
        if not isinstance(event.pattern_match, Match):
            return

        self.page = int(event.pattern_match.group(1))
        await self.update()

    async def update(self):
        await sleep(0.5)

        if self.message is None:
            return

        self._task = None

        buttons = []

        lines = self.content.splitlines()
        total_pages = (len(lines) - 1) // 100

        if self.page > 0:
            buttons.append(Button.inline('Назад', f'log {self.page - 1}'))

        if self.page < total_pages:
            buttons.append(Button.inline('Далее', f'log {self.page + 1}'))

        if buttons:
            buttons = [buttons]

        await self.message.edit(
            '<pre><code class="language-log">'
            f'{'\n'.join(lines[::-1][self.page * 100:(self.page + 1) * 100])}'
            '</code></pre>',
            buttons=buttons
        )
