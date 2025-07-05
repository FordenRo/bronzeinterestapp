import json


with open('config.json', 'r') as f:
    config = json.load(f)


def save_config():
    with open('config.json', 'w') as f:
        json.dump(config, f)
