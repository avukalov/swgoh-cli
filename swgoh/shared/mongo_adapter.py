import os, json
from pymongo import MongoClient, database, collection
from motor.motor_asyncio import AsyncIOMotorClient


class MongoAdapter:

    # _mongoDb: database.Database

    # guilds: collection.Collection
    # players: collection.Collection
    # reports: collection.Collection

    def __init__(self) -> None:
        self.__client = AsyncIOMotorClient(os.getenv('MONGO_URI'))
        self._mongoDb = self.__client['swgoh']
        self.guilds = self._mongoDb['guilds']
        self.players = self._mongoDb['players']
        self.reports = self._mongoDb['reports']

        self.guilds.create_index("profile.id")
        self.players.create_index("guildId")
        self.players.create_index("playerId")
        
    
    # def __await__(self):
    #     return self.init().__await__()

    # async def init(self):
    #     pass

    