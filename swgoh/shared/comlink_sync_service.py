import os
from statistics import median
from swgoh_comlink import SwgohComlink
from swgoh.shared import RedisAdapter, MongoAdapter
from swgoh.shared.models import GuildTwReport, GuildReportKeys

class ComlinkSyncService:
    
    def __init__(self) -> None:
        self._comlink = SwgohComlink(url=os.getenv('COMLINK_URI'))
        self._mongo = MongoAdapter()
        # self._redis = RedisAdapter()
        
        # self._redis = RedisAdapter()
        # self._comlink = SwgohComlink(url=os.getenv('COMLINK_URI'))

    def __await__(self):
        return self.init().__await__()

    async def init(self): 
        self._redis = await RedisAdapter()
        return self
 
    def getGuild(self, id: str, call_api: bool = False) -> dict:

        if not call_api:
            guild = self._redis.hget('guilds', id)
            if guild:
                return guild
               
        guild = self._comlink.getGuild(id)

        # TODO: Add better error hanlding
        if 'code' in guild.keys() and guild['code'] == 32:
            return None
        
        self._redis.hset('guildsByName', guild['profile']['name'], id)

        return guild
    
    async def getGuild2(self, id: str, call_api: bool = False) -> dict:
        
        guildExist = await self._redis.sismember('guilds:ids', id)
        
        # If call_api is False and guildExists is True return guild from cache
        if not call_api and guildExist:
            guild = await self._mongo.guilds.find_one({ 'profile.id': id })
            if guild: return guild
               
        guild = self._comlink.get_guild(id)

        # TODO: Add better error hanlding
        if 'code' in guild.keys() and guild['code'] == 32:
            return None
        
        await self._mongo.guilds.insert_one(guild)

        if not guildExist:
            await self._redis.sadd('guilds:ids', id)
            await self._redis.hset('guilds:names', guild['profile']['name'], id)

        return guild

    async def getGuildMembers(self, id: str, call_api: bool = False) -> dict:
        if not call_api:
            membersIds = await self._redis.smembers(f'guilds:{id}:members')
            members = await self._mongo.players.find_many({})
            if members: return members
                
        members = await self.getGuild(id, call_api)['member']
        
        full_members= []
        for member in members:
            
            self._redis.hset(f'{id}.members', member['playerId'], member)
            
        return full_members
    
    def getPlayer(self, id: str, call_api: bool = False) -> dict:
        
        if not call_api:
            player = self._redis.hget('players', id)
            if player:
                return player
            
        player = self._comlink.getPlayer(player_id=id)
        
        self._redis.hset('players', player['playerId'], player)
        self._redis.hset('players.allyCodes', player['allyCode'], player['playerId'])
        self._redis.hset('players.names', player['name'], player['playerId'])

        return player

    def getGuildReport(self, id: str, key: GuildReportKeys) -> dict | str:
        
        match key:
            case GuildReportKeys.TW:
                report = self._redis.hget('guilds.report.tw', id)
                if not report:
                    return id
                return GuildTwReport(report)
            case GuildReportKeys.TB:
                return self._redis.hget('guilds.report.tb', id)
            case GuildReportKeys.RAID: 
                return self._redis.hget('guilds.report.raid', id)
            case _:
                return None

    def saveTwReport(self, id: str, key: GuildReportKeys, value: GuildTwReport) -> None:
        
        match key:
            case GuildReportKeys.TW:
                self._redis.hset('guilds.report.tw', id, value.__dict__)
                return
            case GuildReportKeys.TB:
                self._redis.hset('guilds.report.tb', id, value.__dict__)
                return 
            case GuildReportKeys.RAID: 
                self._redis.hset('guilds.report.raid', id, value.__dict__)
                return 
            case _:
                return

    def getGuildOverall(self, id: str, call_api: bool = False) -> GuildTwReport | None:
        
        if not call_api:
            guild = self._redis.hget('guilds.overall', id)
            if guild:
                return GuildTwReport(guild)


        guild = self.getGuild(id, call_api)
        if not guild:
            return None

        guild_overall = GuildTwReport()
        guild_overall.name = guild['profile']['name']
        guild_overall.memberCount = guild['profile']['memberCount']
        guild_overall.gp = int(guild['profile']['guildGalacticPower'])
        guild_overall.avgGp = round(guild_overall.gp / guild_overall.memberCount)


        skill_ratings = []
        arena_ranks = []
        fleet_arena_ranks = []

        # TODO: Split implementetion of guild overall and members 
        for member in guild['member']:
            
            # TODO: Move out of here
            member = self._comlink.getPlayer(player_id=member['playerId'])
            if not member:
                continue
            
            self._redis.hset(f'{id}.members', member['playerId'], member)
            # TODO: Move out of here


            
            guild_overall.overall['characterGp'] += int(next((item['value'] for item in member['profileStat'] if item["nameKey"] == "STAT_CHARACTER_GALACTIC_POWER_ACQUIRED_NAME"), 0))
            guild_overall.overall['shipGp'] += int(next((item['value'] for item in member['profileStat'] if item["nameKey"] == "STAT_SHIP_GALACTIC_POWER_ACQUIRED_NAME"), 0))
            
            if member['level'] == 85:
                skill_ratings.append(member['playerRating']['playerSkillRating']['skillRating'])

            arena_ranks.append(member['pvpProfile'][0]['rank'])
            fleet_arena_ranks.append(member['pvpProfile'][1]['rank'])


            # Galactic Legends and TODO: Ships

            for unit in member['rosterUnit']:
                for gl in guild_overall.gls.keys():
                    if gl in unit['definitionId']:
                        guild_overall.gls[gl]['count'] += 1
            
        # TODO: Split implementetion of guild overall and members 
        
        
        guild_overall.overall['medSkillRating'] = median(skill_ratings)
        guild_overall.overall['medCurrArenaRank'] = median(arena_ranks)
        guild_overall.overall['medCurrFleetArenaRank'] = median(fleet_arena_ranks)

        self._redis.hset('guilds.overall', id, guild_overall.__dict__)

        return guild_overall
        
        
