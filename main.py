from client import client
# noinspection PyUnresolvedReferences
from handlers import (repeat_handler, love_emoji_anim, love_show,
                      love_word_anim, magic_anim, stoneface_anim,
                      triple_anim, want_anim, haha_anim)


async def main():
    await client.disconnected


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
