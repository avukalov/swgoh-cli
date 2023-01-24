import os, json
from swgoh.utils import factory


def get_guild_report(guild_name):
    redis = factory.create_redis()
    guild = redis.keys(r'*{guild_name}*')

    report = {
        "count": 0,
        "gls": []
    }

    
    if not guild:
        comlink = factory.create_swgoh_comlink()
        # guild_id = comlink.get_guilds_by_name(guild_name)['guild'][0]['id']
        guild = comlink.get_guild("iC2RW2w_SEWF685Fg4oZwA")

        count = 0
        gls_list = []
        for member in guild['member']:
            player = comlink.get_player(player_id=member['playerId'])
            
            gls = json.loads(redis.get('GLS'))
            for unit in player['rosterUnit']:
                for gl in gls:
                    if f"{gl}:SEVEN_STAR" == unit['definitionId']:
                        count += 1
                        gls_list.append(gl)
        report['count'] = count
        report['gls'] = gls_list
    return report
        



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