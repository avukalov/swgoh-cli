import os
from statistics import median
from swgoh_comlink import SwgohComlink
from swgoh.services import CacheManager 
from swgoh.models import GuildTwReport, GuildReportKeys

class ComlinkSyncService:
    
    def __init__(self) -> None:
        self._cache = CacheManager()
        self._comlink = SwgohComlink(url=os.getenv('COMLINK_URI'))
        
        # self._cache = CacheManager()
        # self._comlink = SwgohComlink(url=os.getenv('COMLINK_URI'))

 
    def get_guild(self, id: str, call_api: bool = False) -> dict:

        if not call_api:
            guild = self._cache.hget('guilds', id)
            if guild:
                return guild
               
        guild = self._comlink.get_guild(id)

        # TODO: Add better error hanlding
        if 'code' in guild.keys() and guild['code'] == 32:
            return None
        
        self._cache.hset('guilds', id, guild)

        return guild

    def get_guild_members(self, id: str, call_api: bool = False) -> dict:
        if not call_api:
            membersKeys = self._cache.hkeys(f'{id}.members')
            members = [self._cache.hget('players', id) for id in membersKeys]
            if members:
                return members
                
        members = self.get_guild(id, call_api)['member']
        
        full_members= []
        for member in members:
            self._cache.hset(f'{id}.members', member['playerId'], member)
            full_members.append(self.get_player(member['playerId']))
            
        return full_members
    
    def get_player(self, id: str, call_api: bool = False) -> dict:
        
        if not call_api:
            player = self._cache.hget('players', id)
            if player:
                return player
            
        player = self._comlink.get_player(player_id=id)
        
        self._cache.hset('players', player['playerId'], player)
        self._cache.hset('players.allyCodes', player['allyCode'], player['playerId'])
        self._cache.hset('players.names', player['name'], player['playerId'])

        return player

    def get_guild_report(self, id: str, key: GuildReportKeys) -> dict | str:
        
        match key:
            case GuildReportKeys.TW:
                report = self._cache.hget('guilds.report.tw', id)
                if not report:
                    return id
                return GuildTwReport(report)
            case GuildReportKeys.TB:
                return self._cache.hget('guilds.report.tb', id)
            case GuildReportKeys.RAID: 
                return self._cache.hget('guilds.report.raid', id)
            case _:
                return None

    def save_report(self, id: str, key: GuildReportKeys, value: GuildTwReport) -> None:
        
        match key:
            case GuildReportKeys.TW:
                self._cache.hset('guilds.report.tw', id, value.__dict__)
                return
            case GuildReportKeys.TB:
                self._cache.hset('guilds.report.tb', id, value.__dict__)
                return 
            case GuildReportKeys.RAID: 
                self._cache.hset('guilds.report.raid', id, value.__dict__)
                return 
            case _:
                return

    def get_guild_overall(self, id: str, call_api: bool = False) -> GuildTwReport | None:
        
        if not call_api:
            guild = self._cache.hget('guilds.overall', id)
            if guild:
                return GuildTwReport(guild)


        guild = self.get_guild(id, call_api)
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
            member = self._comlink.get_player(player_id=member['playerId'])
            if not member:
                continue
            
            self._cache.hset(f'{id}.members', member['playerId'], member)
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

        self._cache.hset('guilds.overall', id, guild_overall.__dict__)

        return guild_overall
        
        
