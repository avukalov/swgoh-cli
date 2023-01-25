import time
from swgoh.classes import ComlinkManager


class GuildManager:

    def __init__(self) -> None:
        self.comlink_manager = ComlinkManager()
        
        self.guilds = []


    def compare(self, guilds_to_compare: list, force: bool = False):
        
        guilds = []

        for guild_id in guilds_to_compare:
            
            # start = time.time()
            # end = time.time()
            # print(end - start)

            guild = self.comlink_manager.get_guild_overall(guild_id, force)
            guilds.append(guild)

        return guilds

        

        