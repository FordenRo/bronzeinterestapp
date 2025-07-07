import os
import json


help_messages = {
    'online':
    r'<code>be|no online</code> - <i>включить|выключить постоянный онлайн</i>\n'
    r'<code>online state|status</code> - <i>проверить статус постоянного онлайна</i>\n'
    r'<code>online help</code> - <i>справка по онлайну</i>',

    'spy':
    r'<code>spy online|read @username onetime?</code> - <i>следить за онлайном|чтением</i>\n'
    r'<code>spy remove online|read @username</code> - <i>убрать из слежения</i>\n'
    r'<code>spy list</code> - <i>список пользователей в слежении</i>\n'
    r'<code>spy help</code> - <i>справка по слежению</i>',

    'autoresponder':
    r'<code>autoresponder @nickname silent? onetime? text</code> - <i>настроить автоответ</i>\n'
    r'<code>autoresponder remove @nickname</code> - <i>убрать автоответ</i>\n'
    r'<code>autoresponder list</code> - <i>список пользователей в автоответчике</i>\n'
    r'<code>autoresponder help</code> - <i>справка по автоответчику</i>',

    'autoreader':
    r'<code>autoreader @nickname silent? onetime?</code> - <i>автоматически читать сообщения</i>\n'
    r'<code>autoreader remove @nickname</code> - <i>убрать авточитатель</i>\n'
    r'<code>autoreader list</code> - <i>список пользователей в авточитателе</i>\n'
    r'<code>autoreader help</code> - <i>справка по авточитателю</i>',

    'log':
    r'<code>log send</code> - <i>отправить файл с логом</i>\n'
    r'<code>log clear|cls</code> - <i>очистить лог</i>\n'
    r'<code>log help</code> - <i>справка по логам</i>',

    'system':
    r'<code>stop</code> - <i>остановить бота</i>\n'
    r'<code>restart</code> - <i>перезапустить бота</i>\n'
    r'<code>update</code> - <i>обновить и перезапустить</i>\n'
    r'<code>update check</code> - <i>проверить доступные обновления</i>',
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
