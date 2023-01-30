import os, json
from redis import Redis

class RedisAdapter():

    def __init__(self) -> None:
        self.__redis = Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            password=os.getenv('REDIS_PASSWORD'),
            db=1
        )

        # Register Lua scripts
        # self.__redis.register_script()
        

    # Key -> Value
    def get(self, key: str) -> any:
        return json.loads(self.__redis.get(key))

    def set(self, key: str, value: any) -> bool | None:
        return self.__redis.set(key, json.dumps(value))

    def keys(self, pattern: str) -> list:
        keys = self.__redis.keys(pattern)
        if not keys:
            return []
        return [key.decode('utf-8') for key in keys]
    

    # Set
    def sadd(self, set_key: str, value: any):
        # self.__redis
        return self.__redis.sadd(set_key, json.dumps(value))
    

    # Hashset
    def hget(self, name: str, key: str) -> dict | None:
        
        guild = self.__redis.hget(name, key);
        if guild:
            return json.loads(guild)
        return None

    def hgetall(self, name: str) -> dict:
        return json.loads(self.__redis.hgetall(name))

    def hset(self, name: str, key: str, value: any):
        return self.__redis.hset(name, key, json.dumps(value))

    def hkeys(self, name: str) -> list:
        keys = self.__redis.hkeys(name)
        if not keys:
            return []
        return [key.decode('utf-8') for key in keys]

    def hvals(self, name: str) -> dict:
        return [json.loads(val) for val in self.__redis.hvals(name)]
    
    def hdel(self, name: str, key: str):
        # TODO: Test what is 'any'
        return self.hdel(name, key)

    
