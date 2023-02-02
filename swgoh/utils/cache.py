import os, json
from datetime import datetime, timedelta
from swgoh.utils import factory

def load_initial_cache():
    
    cache_metadata()
    cache_guild()
    cache_guild_members()

    
        
def cache_guild() -> None:
    redis = factory.create_redis()
    
    guild_name = os.getenv('GUILD_NAME')
    guild_id = os.getenv('GUILD_ID')

    keys = redis.keys(rf'*{guild_name}*')

    if not keys:
        fetch_guild_data_and_cache(guild_id)
    
    else:
        # guild.<guild_name>.<datetime>
        latest = datetime.strptime(keys[-1].decode("utf-8").split('.')[-1], '%Y-%m-%d').date()
        
        if datetime.now().date() - timedelta(days=7) >= latest:
            fetch_guild_data_and_cache(guild_id)


def cache_guild_members():
    redis = factory.create_redis()
    comlink = factory.create_swgoh_comlink()

    guild_name = os.getenv('GUILD_NAME')

    guild_keys = redis.keys(rf'*{guild_name}*')
    player_keys = redis.keys(rf'{guild_name}\.\d+{9}.')
    print(guild_keys)
    print(player_keys)

    if player_keys or not guild_keys:
        print("exit")
        return
    
    guild = json.loads(redis.get(guild_keys[-1]))

    for member in guild['member']:
        player = comlink.get_player(player_id=member['playerId'], enums=True)
        key = create_key(
            key=player['allyCode'],
            prefix=guild_name)
        redis.set(key, json.dumps(player))
        break


def fetch_guild_data_and_cache(guild_id: str) -> None:
    redis = factory.create_redis()
    comlink = factory.create_swgoh_comlink()

    guild_data = comlink.get_guild(
        guild_id,
        include_recent_guild_activity_info=True,
        enums=True
    )
    print("Comlink called")

    key = create_key(
        key=guild_data['profile']['name'],
        prefix='guild',
        suffix=str(datetime.now().date())
    )

    redis.set(key, json.dumps(guild_data))


def cache_metadata():
    redis = factory.create_redis()

    gls = [gl.replace(' ', '').upper() for gl in [
        'Jabba the Hutt',
        'Jedi Master Kenobi',
        'Jedi Master Luk Skywalker',
        'Lord Vader',
        'GL Rey',
        'Sith Eternal Emperor',
        'Supreme Leader Kylo Ren'
    ]]

    redis.set('GLS', json.dumps(gls))


def create_key(key: str, prefix: str = "", suffix: str = "") -> str:
    key_builder = []
    key_builder.append(prefix)
    key_builder.append(key)
    key_builder.append(suffix)
    
    return '.'.join(key_builder)

