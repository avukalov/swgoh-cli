import os, json
from redis import Redis

class CacheManager:

    def __init__(self) -> None:
        self.redis = Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            password=os.getenv('REDIS_PASSWORD'),
            db=1
        )

        # self.redis.register_script()

    # Key -> Value
    def get(self, key: str) -> any:
        return json.loads(self.redis.get(key))

    def set(self, key: str, value: any) -> bool | None:
        return self.redis.set(key, json.dumps(value))

    def keys(self, pattern: str) -> list:
        keys = self.redis.keys(pattern)
        if not keys:
            return []
        return [key.decode('utf-8') for key in keys]
    

    # Set
    def sadd(self, set_key: str, value: any):
        # self.redis
        return self.redis.sadd(set_key, json.dumps(value))
    

    # Hashset
    def hset(self, name: str, key: str, value: any):
        return self.redis.hset(name, key, json.dumps(value))


    def hget(self, name: str, key: str) -> (dict | None):
        
        guild = self.redis.hget(name, key);
        if guild:
            return json.loads(guild)
        return None
        
        
    def hkeys(self, name: str) -> list:
        keys = self.redis.hkeys(name)
        if not keys:
            return []
        return [key.decode('utf-8') for key in keys]
    
    def hdel(self, name: str, key: str):
        # TODO: Test what is 'any'
        return self.hdel(name, key)

    
