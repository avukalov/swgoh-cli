import requests, json
from typing import Tuple
from swgoh.models import GuildReportKeys, TBKeys, UnitBase, PlayerBase
from swgoh.services import ComlinkSyncService
from swgoh.builders import TWReportBuilder
from swgoh.models import GuildTwReport
from swgoh.utils import config


class GuildService(ComlinkSyncService):

    def __init__(self) -> None:
        ComlinkSyncService.__init__(self)


    def compare(self, ids: Tuple[str, str], call_api: bool = False) -> list[GuildTwReport | None]:
        
        missing_reports = [id for id in ids]
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
                builder.add_member_stats(player)
            
            builder.add_total_ratings()
            reports.append(builder.build())
        
        for report in reports:
            self.save_report(report.id, GuildReportKeys.TW, report)

        return reports

    # TODO: Add match case for diferent TB
    def get_hoth_requirements(self, id, call_api: bool = False):
        
        # TODO: Export it
        territory_battle = config['TB'][TBKeys.DSHOTH.value]['battles']['PROBE_DROID']
        
        members = self.get_guild_members(id, call_api)

        members_rosters = []
        for member in members:
            roster = []
            for unit in member['rosterUnit']:
                unit_name = unit['definitionId'].split(':')[0]
                if unit_name in config['category'][territory_battle['requiremants']['category_req']]:
                    roster.append(unit)

            r = requests.post(
                    'http://server:3201/api?flags=onlyGP',
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(roster)
                )

            sorted_response: list[UnitBase] = []
            for unit in json.loads(r.text):
                u = UnitBase()
                u.name = config['imperial_troopers'][unit['definitionId'].split(':')[0]]
                u.gp = unit['gp']
                u.stars = unit['currentRarity']
                u.gear = unit['currentTier']
                u.level = unit['currentLevel']
                sorted_response.append(u)
            
            player = PlayerBase()
            player.id = member['playerId']
            player.allyCode = member['allyCode']
            player.name = member['name']
            player.gp = int([stat['value'] for stat in member['profileStat'] if stat['nameKey'] == "STAT_GALACTIC_POWER_ACQUIRED_NAME"][0])
            player.roster = sorted(sorted_response, key=lambda unit: unit.gp, reverse=True)

            members_rosters.append(player)
        
        return sorted(members_rosters, key=lambda p: p.gp)


        