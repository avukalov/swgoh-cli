import json


def format_long_number(number: int) -> str:
        return "{:,}".format(number)

def format_allyCode(allyCode: int):
        return '-'.join(str(allyCode[i:i+3]) for i in range(0, len(allyCode), 3))

def get_config() -> dict:
        
        config = {}

        with open('./swgoh/utils/game_data.json', 'r') as game_data:
                config = json.load(game_data)

        return config


config = get_config()