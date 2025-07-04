from collections.abc import Callable, Coroutine

from telethon.events import MessageRead
from telethon.tl.custom import Message

from client import client


def register_on_read_event(message: Message, func: Callable[[Message], Coroutine]):
    @client.on(MessageRead([message.chat_id]))
    async def on_read(event):
        if not event.is_read(message.id):
            return

        client.loop.create_task(func(message))
        client.remove_event_handler(on_read)
