from telethon import TelegramClient

client = TelegramClient('Interest', 21054109, 'a273f829f04abde273f1869c9762446f')
cmd_block = False


def set_cmd_block(state: bool):
    global cmd_block

    cmd_block = state
