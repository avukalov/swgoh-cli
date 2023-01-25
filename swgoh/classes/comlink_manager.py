import os
from statistics import median
from swgoh_comlink import SwgohComlink
from swgoh.classes import CacheManager 
from swgoh.models import GuildOverall

class ComlinkManager:

    def __init__(self) -> None:
        self.cache = CacheManager()
        self.comlink = SwgohComlink(url=os.getenv('COMLINK_URI'))
 
    
    def get_guild(self, guild_id: str, force: bool = False) -> dict:
        
        if not force:
            guild = self.cache.hget('guilds', guild_id)
            if guild:
                return guild
               

        guild = self.comlink.get_guild(guild_id)
        
        # TODO: Add better error hanlding
        if 'code' in guild.keys() and guild['code'] == 32:
            return None
        
        self.cache.hset('guilds', guild_id, guild)

        return guild


    def get_guild_overall(self, guild_id: str, force: bool = False):
        
        if not force:
            guild = self.cache.hget('guilds.overall', guild_id)
            if guild:
                return GuildOverall(guild)


        guild = self.get_guild(guild_id, force)
        if not guild:
            return None

        guild_overall = GuildOverall()
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
            member = self.comlink.get_player(player_id=member['playerId'])
            if not member:
                continue
            
            self.cache.hset(f'{guild_id}.members', member['playerId'], member)
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

        self.cache.hset('guilds.overall', guild_id, guild_overall.__dict__)

        return guild_overall
        
        
