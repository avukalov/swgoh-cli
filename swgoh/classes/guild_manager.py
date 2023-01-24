import time
from swgoh.classes import ComlinkManager


class GuildManager:

    def __init__(self) -> None:
        self.comlink_manager = ComlinkManager()


        self.guilds = []
        self.guild = {
            'name': '',
            'gp': '',
            'avgGp': '',
            'gls': [],
            'ships': [],
            'overall': {
                'characterGp': 0,
                'shipGp': 0,
                'avgSkillRating': 0,
                'avgCurrArenaRank': 0,
                'avgCurrFleetArenaRank': 0
            }
        }


    def compare(self, guilds_to_compare: list, force: bool = False):
        
        guilds = []

        for guild_id in guilds_to_compare:
            
            guild = self.comlink_manager.get_guild_overall(guild_id, force)
            guilds.append(guild)

            
            # start = time.time()
            # end = time.time()
            # print(end - start)

        return guilds

        

        