from swgoh.models import GuildTwReport
from statistics import median

class TWReportBuilder:

    def __init__(self) -> None:
        self.__guild = GuildTwReport()
        self.__skill_ratings = []
        self.__arena_ranks = []
        self.__fleet_arena_ranks = []

    
    def add_guild_stats(self, guild: dict) -> None:

        self.__guild.id = guild['profile']['id']
        self.__guild.name = guild['profile']['name']
        self.__guild.memberCount = guild['profile']['memberCount']
        self.__guild.gp = int(guild['profile']['guildGalacticPower'])
        self.__guild.avgGp = self.__guild.gp // self.__guild.memberCount


    def add_member_stats(self, member: dict) -> None:
        
        self.__guild.overall['characterGp'] += int(next((item['value'] for item in member['profileStat'] if item["nameKey"] == "STAT_CHARACTER_GALACTIC_POWER_ACQUIRED_NAME"), 0))
        self.__guild.overall['shipGp'] += int(next((item['value'] for item in member['profileStat'] if item["nameKey"] == "STAT_SHIP_GALACTIC_POWER_ACQUIRED_NAME"), 0))

        if member['level'] == 85:
                self.__skill_ratings.append(member['playerRating']['playerSkillRating']['skillRating'])

        self.__arena_ranks.append(member['pvpProfile'][0]['rank'])
        self.__fleet_arena_ranks.append(member['pvpProfile'][1]['rank'])

        for unit in member['rosterUnit']:
            for gl in self.__guild.gls.keys():
                if gl in unit['definitionId']:
                    self.__guild.gls[gl]['count'] += 1


    def add_total_ratings(self) -> None:
        self.__guild.overall['medSkillRating'] = median(self.__skill_ratings)
        self.__guild.overall['medCurrArenaRank'] = median(self.__arena_ranks)
        self.__guild.overall['medCurrFleetArenaRank'] = median(self.__fleet_arena_ranks)
    
    
    def reset(self) -> None:
        self.__guild = GuildTwReport()
        self.__skill_ratings = []
        self.__arena_ranks = []
        self.__fleet_arena_ranks = []

    
    def build(self) -> GuildTwReport:
        return self.__guild