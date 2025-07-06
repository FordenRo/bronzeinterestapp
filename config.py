import os
import json


help_messages = {
    'online': 'be|no online - <i>включить|выключить постоянный онлайн</i>\n'
    'online state|status - <i>проверить статус постоянного онлайна</i>\n'
    'online help - <i>справка по онлайну</i>',

    'spy': 'spy online|read @username onetime? - <i>следить за онлайном|чтением пользователя</i>\n'
           'spy remove online|read @username - <i>убрать из слежения</i>\n'
           'spy list - <i>список пользователей в слежении</i>\n'
           'spy help - <i>справка по слежению</i>',

    'autoresponder': 'autoresponder @nickname silent? text - <i>настроить автоответ</i>\n'
                     'autoresponder remove @nickname - <i>убрать автоответ</i>\n'
                     'autoresponder list - <i>список пользователей в автоответчике</i>\n'
                     'autoresponder help - <i>справка по автоответчику</i>',

    'autoreader': 'autoreader @nickname silent? onetime? - <i>автоматически читать сообщения</i>\n'
                  'autoreader remove @nickname - <i>убрать авточитатель</i>\n'
                  'autoreader list - <i>список пользователей в авточитателе</i>\n'
                  'autoreader help - <i>справка по авточитателю</i>',

    'log': 'log send - <i>отправить файл с логом</i>\n'
           'log clear|cls - <i>очистить лог</i>\n'
           'log help - <i>справка по логам</i>',

    'system': 'stop - <i>остановить бота</i>\n'
              'restart - <i>перезапустить бота</i>\n'
              'update - <i>обновить и перезапустить</i>\n'
              'update check - <i>проверить доступные обновления</i>',
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
