import os
import json


help_messages = {
    'online': '<code>be|no online</code> - <i>включить|выключить постоянный онлайн</i>\n'
    '<code>online state|status</code> - <i>проверить статус постоянного онлайна</i>\n'
    '<code>online help</code> - <i>справка по онлайну</i>',

    'spy': '<code>spy online|read @username onetime?</code> - <i>следить за онлайном|чтением пользователя</i>\n'
           '<code>spy remove online|read @username</code> - <i>убрать из слежения</i>\n'
           '<code>spy list</code> - <i>список пользователей в слежении</i>\n'
           '<code>spy help</code> - <i>справка по слежению</i>',

    'autoresponder': '<code>autoresponder @nickname silent? text</code> - <i>настроить автоответ</i>\n'
                     '<code>autoresponder remove @nickname</code> - <i>убрать автоответ</i>\n'
                     '<code>autoresponder list</code> - <i>список пользователей в автоответчике</i>\n'
                     '<code>autoresponder help</code> - <i>справка по автоответчику</i>',

    'autoreader': '<code>autoreader @nickname silent? onetime?</code> - <i>автоматически читать сообщения</i>\n'
                  '<code>autoreader remove @nickname</code> - <i>убрать авточитатель</i>\n'
                  '<code>autoreader list</code> - <i>список пользователей в авточитателе</i>\n'
                  '<code>autoreader help</code> - <i>справка по авточитателю</i>',

    'log': '<code>log send</code> - <i>отправить файл с логом</i>\n'
           '<code>log clear|cls</code> - <i>очистить лог</i>\n'
           '<code>log help</code> - <i>справка по логам</i>',

    'system': '<code>stop</code> - <i>остановить бота</i>\n'
              '<code>restart</code> - <i>перезапустить бота</i>\n'
              '<code>update</code> - <i>обновить и перезапустить</i>\n'
              '<code>update check</code> - <i>проверить доступные обновления</i>',
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
