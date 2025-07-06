import os
import json


help_messages = {
    'online': 'be|no online - включить|выключить постоянный онлайн\n'
    'online state|status - проверить статус постоянного онлайна\n'
    'online help - справка по онлайну',

    'spy': 'spy online|read @username onetime? - следить за онлайном|чтением пользователя\n'
           'spy remove online|read @username - убрать из слежения\n'
           'spy list - список пользователей в слежении\n'
           'spy help - справка по слежению',

    'autoresponder': 'autoresponder @nickname silent? text - настроить автоответ\n'
                     'autoresponder remove @nickname - убрать автоответ\n'
                     'autoresponder list - список пользователей в автоответчике\n'
                     'autoresponder help - справка по автоответчику',

    'autoreader': 'autoreader @nickname silent? onetime? - автоматически читать сообщения\n'
                  'autoreader remove @nickname - убрать авточитатель\n'
                  'autoreader list - список пользователей в авточитателе\n'
                  'autoreader help - справка по авточитателю',

    'log': 'log send - отправить файл с логом\n'
           'log clear|cls - очистить лог\n'
           'log help - справка по логам',

    'system': 'stop - остановить бота\n'
              'restart - перезапустить бота\n'
              'update - обновить и перезапустить\n'
              'update check - проверить доступные обновления',
}

if not os.path.exists('config.json'):
    with open('config.json', 'w') as f:
        json.dump({}, f)
        config = {}
else:
    with open('config.json', 'r') as f:
        config = json.load(f)


def save_config():
    with open('config.json', 'w') as f:
        json.dump(config, f)
