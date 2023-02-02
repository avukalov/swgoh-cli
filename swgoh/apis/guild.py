import os, json
from swgoh.utils import factory


def get_players_guild_requirements():
    
    client = factory.create_swgoh_comlink()
    #return os.getenv('GUILD_ID')
    response = client.get_guild(guild_id=os.getenv('GUILD_ID'))

    ROSTER_REPORT = []
    for member in response['member']:
        
        player = client.get_player(player_id=member['playerId'])
        
        player_report = {
            'name': player['name'],
            'allyCode': player['allyCode'],
            'units': []
        }
        
        units = []
        for unit in player['rosterUnit']:
            if 'VEERS' in unit['definitionId'] and unit['currentTier'] < 10:
                units.append({
                    'name': 'Veers',
                    'stars': unit['currentRarity'],
                    'level': unit['currentLevel'],
                    'gear': unit['currentTier'],
                })
            if 'STARCK' in unit['definitionId'] and unit['currentTier'] < 10:
                units.append({
                    'name': 'Starck',
                    'stars': unit['currentRarity'],
                    'level': unit['currentLevel'],
                    'gear': unit['currentTier'],
                })
        player_report['units'] = units
        ROSTER_REPORT.append(player_report)
        break

    return ROSTER_REPORT