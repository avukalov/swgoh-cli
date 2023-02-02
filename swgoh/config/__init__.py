from swgoh.config.config import config as config_group


import json


def formatLongNumber(number: int) -> str:
        return "{:,}".format(number)

def formatAllyCode(allyCode: int):
        return '-'.join(str(allyCode[i:i+3]) for i in range(0, len(allyCode), 3))

def getConfig() -> dict:
        
        config = {}

        with open('./swgoh/config/game_data.json', 'r') as gameData:
                config = json.load(gameData)

        return config


config = getConfig()