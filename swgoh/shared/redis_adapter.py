import os, json
from redis.asyncio import BlockingConnectionPool, Redis

class RedisAdapter():

    def __init__(self) -> None:
        self.__pool = BlockingConnectionPool(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True,
            db=1
        )
        
    def __await__(self):
        return self.init().__await__()

    async def init(self):
        self._redis: Redis = await Redis(connection_pool=self.__pool)
        # Register Lua scripts
        # self._redis.register_script()
        return self


    # KEY - VALUE
    async def get(self, key: str) -> any:
        return json.loads(await self._redis.get(key))

    async def set(self, key: str, value: any) -> bool | None:
        return await self._redis.set(key, json.dumps(value))
    
    async def delete(self, key: str):
        return await self._redis.delete(key)

    async def keys(self, pattern: str) -> list:
        return [key.decode('utf-8') for key in await self._redis.keys(pattern)]
    

    # SET
    async def sadd(self, set_key: str, value: any):
        return await self._redis.sadd(set_key, json.dumps(value))
    
    async def sismember(self, key: str, value: any):
        return await self._redis.sismember(key, json.dumps(value))

    async def smembers(self, key: str):
        return [json.loads(value) for value in await self._redis.smembers(key)]

    # HASHSET
    async def hget(self, name: str, key: str) -> dict | None:
        guild = await self._redis.hget(name, key)
        return json.loads(guild) if guild else None
        
    async def hgetall(self, name: str) -> dict:
        return json.loads(await self._redis.hgetall(name))

    async def hset(self, name: str, key: str, value: any):
        return await self._redis.hset(name, key, json.dumps(value))

    async def hkeys(self, name: str) -> list:
        return [key.decode('utf-8') for key in await self._redis.hkeys(name)]

    async def hvals(self, name: str) -> dict:
        return [json.loads(val) for val in await self._redis.hvals(name)]
    
    async def hdel(self, name: str, key: str) -> int:
        return await self._redis.hdel(name, key)

    
