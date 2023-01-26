import os
from typing import Tuple
from swgoh.models import GuildReportKeys
from swgoh.services import ComlinkSyncService
from swgoh.builders import TWReportBuilder
from swgoh.models import GuildTwReport


class GuildService(ComlinkSyncService):

    def __init__(self) -> None:
        ComlinkSyncService.__init__(self)
        

    def compare(self, ids: Tuple[str, str], call_api: bool = False) -> list[GuildTwReport | None]:
        
        return [self.get_guild_overall(id, call_api) for id in ids]

    def compare_2(self, ids: Tuple[str, str], call_api: bool = False) -> list[GuildTwReport | None]:
        
        missing_reports = []
        if not call_api:
            
            reports = [self.get_guild_report(id, GuildReportKeys.TW) for id in ids]
            missing_reports = [r for r in reports if r in ids]

            if len(missing_reports) == 0:
                return reports
        
        guilds = [self.get_guild(id, call_api) for id in missing_reports]

        reports: list[GuildTwReport] = []
        for guild in guilds: 
            builder = TWReportBuilder()
            builder.add_guild_stats(guild)

            members = self.get_guild_members(guild['profile']['id'])
            for member in members:
                player = self.get_player(member['playerId'], call_api)
                builder.add_members_stats(player)
            
            builder.add_total_ratings()
            reports.append(builder.build())
        
        for report in reports:
            self.save_report(report.id, GuildReportKeys.TW, report)

        return reports


# class GuildTwReportReportBuilder:
#     def __init__(self) -> None:
#         pass

#     def set_guild_overall():
#         pass

#     def set_members_overall():
#         pass

#     def set_gls_overall():
#         pass

#     def set_ships_overall():
#         pass