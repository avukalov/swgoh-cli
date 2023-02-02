import requests, json
from typing import Tuple
from swgoh.shared.models import GuildTwReport, GuildReportKeys, TBKeys, UnitBase, PlayerBase
from swgoh.shared import ComlinkSyncService
from swgoh.guild.tw_report_builder import TWReportBuilder
from swgoh.config import config


class GuildManager(ComlinkSyncService):

    def __init__(self) -> None:
        ComlinkSyncService.__init__(self)


    async def compare(self, ids: Tuple[str, str], call_api: bool = False) -> list[GuildTwReport | None]:
        
        missing_reports = [id for id in ids]
        if not call_api:
            
            reports = [await self.getGuildReport(id, GuildReportKeys.TW) for id in ids]
            missing_reports = [r for r in reports if r in ids]

            if len(missing_reports) == 0:
                return reports
        
        guilds = [await self.getGuild2(id, call_api) for id in missing_reports]

        reports: list[GuildTwReport] = []
        for guild in guilds: 
            builder = TWReportBuilder()
            builder.add_guild_stats(guild)

            membersIds = await self.getGuildMembers(guild['profile']['id'])
            for id in membersIds:
                player = await self.getPlayer(id, call_api)
                builder.add_member_stats(player)
            
            builder.add_total_ratings()
            reports.append(builder.build())
        
        for report in reports:
            await self.saveTwReport(report.id, GuildReportKeys.TW, report)

        return reports

    # TODO: Add match case for diferent TB
    def get_hoth_requirements(self, id, call_api: bool = False):
        
        # TODO: Export it
        territory_battle = config['TB'][TBKeys.DSHOTH.value]['battles']['PROBE_DROID']
        
        members = self.getGuildMembers(id, call_api)

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

            counter = 0
            counter_roster = []

            units_list: list[UnitBase] = []
            for unit in json.loads(r.text):
                if(counter >= 3 and 'VEERS' in counter_roster and 'COLONESTARCK' in counter_roster):
                    break

                if (unit['currentRarity'] == 7 and unit['currentTier'] > 10 and unit['currentLevel'] >= 80) or int(unit['gp']) > 13300:
                        counter += 1
                        counter_roster.append(unit_name)

                u = UnitBase()
                u.name = config['imperial_troopers'][unit['definitionId'].split(':')[0]]
                u.gp = unit['gp']
                u.stars = unit['currentRarity']
                u.gear = unit['currentTier']
                u.level = unit['currentLevel']
                units_list.append(u)
            
            if counter >= 3:
                continue

            player = PlayerBase()
            player.id = member['playerId']
            player.allyCode = member['allyCode']
            player.name = member['name']
            player.gp = int([stat['value'] for stat in member['profileStat'] if stat['nameKey'] == "STAT_GALACTIC_POWER_ACQUIRED_NAME"][0])
            player.roster = sorted(units_list, key=lambda unit: unit.gp, reverse=True)

            members_rosters.append(player)
            # break
        
        return sorted(members_rosters, key=lambda p: p.gp)

    # def filter_members_tb(unit) -> int:

    #     if unit['currentRarity'] == 7 and unit['currentTier'] > 10 and unit['currentLevel'] >= 80:
    #             return 1
    #     unit_name = unit['definitionId'].split(':')[0]
    #     if unit_name in ['VEERS', 'COLONESTARCK']:
            
    #     return 0

        