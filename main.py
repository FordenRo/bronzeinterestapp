from client import client
# noinspection PyUnresolvedReferences
from handlers import love_show, love_emoji_anim, love_word_anim, magic_anim


async def main():
    await client.disconnected


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
