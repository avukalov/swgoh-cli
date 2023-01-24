import os
from redis import Redis
from swgoh_comlink import SwgohComlink
from swgoh.classes import cache_manager


def create_swgoh_comlink() -> SwgohComlink:
    return SwgohComlink(url=os.getenv('COMLINK_URI'))

def create_redis() -> Redis:
    return Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        password=os.getenv('REDIS_PASSWORD'),
        db=1
    )

def get_redis_client():
    return cache_manager.RedisClient()