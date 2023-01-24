import os
from swgoh.utils import factory

def get_player():
    
    client = factory.create_swgoh_comlink()

    response = client.get_player(
        allycode=None,
        player_id=os.getenv('PLAYER_ID')
    )

    return response