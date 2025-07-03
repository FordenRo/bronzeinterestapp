from asyncio import gather, sleep
from math import cos

from telethon.events import NewMessage
from telethon.tl.custom import Message

from client import client
from utils import lerp


@client.on(NewMessage(outgoing=True, pattern='lstart'))
async def command(message: Message):
    client.loop.create_task(start(message))


async def respond(message: Message, text: str):
    if message:
        return await message.respond(f'`{text}`', parse_mode='markdown')
    else:
        print(text)


def cl_cos(x):
    return (cos(x) + 1) / 2


async def start(message: Message):
    mps = 10

    dl = 1 / mps
    w = 27

    for i in range(5):
        await respond(message, '.' * w)
        await sleep(dl)

    x = 0
    for i in range(31):
        l = list('.' * w)
        x = round(cl_cos(i / 30 * 10) * (w - 2))
        x2 = (w - 2) - x
        l[x:x + 2] = list('❤️')
        l[x2:x2 + 2] = list('💜️')
        await respond(message, ''.join(l))
        await sleep(dl)

    for i in range(11):
        l = list('.' * w)
        t = i / 10
        a1 = round(lerp(x, w - 2, pow(t * 0.7 + 0.3, 2)))
        a2 = (w - 2) - a1
        l[a1:a1 + 2] = list('❤️')
        l[a2:a2 + 2] = list('💜️')
        await respond(message, ''.join(l))
        await sleep(dl)

    for i in range(5):
        l = list('.' * w)
        x = i % 2 * (w - 2)
        x2 = (w - 2) - x
        l[x:x + 2] = '❤️'
        l[x2:x2 + 2] = '💜️'
        await respond(message, ''.join(l))
        await sleep(dl)

    await respond(message, '.' * w)
    await sleep(dl)

    m = 'люблю'
    for i in range(1, len(m)):
        l = list('.' * w)
        l[:i] = list(m)[len(m) - i:]
        l[-i:] = list(m)[:i]
        await respond(message, ''.join(l))
        await sleep(dl)

    hearts = []
    for i in range(150):
        l = list('.' * w)
        x1 = round(cl_cos(i / 5) * (w - len(m)))
        x2 = (w - len(m)) - x1
        l[x1:x1 + 5] = list(m)
        l[x2:x2 + 5] = list(m)
        if i % 5 == 0 and 20 < i < 143:
            hearts += [(w, '❤️' if i % 10 == 0 else '💜️')]
        hearts = list(filter(lambda x: x[0] >= 0, map(lambda x: (x[0] - 4, x[1]), hearts)))
        for p in hearts:
            l[p[0]:p[0] + 2] = p[1]
        await respond(message, ''.join(l))
        await sleep(dl)

    ly = 'люблю.тебя'
    for i in range(6, len(ly) + 1):
        await respond(message, f'{ly[:i]:.^{w}s}')
        await sleep(dl * 2)

    await respond(message, f'{'малышка':.^{w}s}')
    await sleep(dl * 2)

    await respond(message, f'{'моя)':.^{w}s}')
    await sleep(dl * 2)

    await respond(message, '.' * w)
    await sleep(dl * 2)

    for i in range(10):
        if i % 2 == 0:
            await respond(message, f'{'LOVE':.^{w}s}')
        else:
            await respond(message, 'LOVE' + '.' * (w - 8) + 'LOVE')
        await sleep(dl * 2)

    await respond(message, '.' * w)
    await sleep(dl * 2)

    heart = ['......####.......####......',
             '....########...########....',
             '.#########################.',
             '###########################',
             '..#######################..',
             '....###################....',
             '.......#############.......',
             '..........#######..........']

    messages: list[Message] = []
    for i in heart:
        messages += [await respond(message, i)]
        await sleep(dl * 2)

    if message:
        for c in range(15):
            tasks = []
            for i, msg in enumerate(messages):
                hm = heart[i]
                if c % 2 == 0:
                    hm = hm.replace('#', '$')
                tasks += [msg.edit(f'`{hm}`', parse_mode='markdown')]
            await gather(*tasks)
            await sleep(1)
