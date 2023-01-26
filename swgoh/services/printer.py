import os
from swgoh import console
from swgoh.utils import format_long_number
from swgoh.models import GuildTwReport

from rich.console import Console
from rich.text import Text
from rich.box import Box, SQUARE, DOUBLE
from rich.table import Table
from rich.panel import Panel



class Printer:
    def __init__(self) -> None:
        self.console = console
        pass
    
    def export_svg(self, path: str, guilds_name: list[str]) -> None:
        g = [name.replace(' ', '_') for name in guilds_name]

        console.save_svg(
            title="TW Report",
            path=f"{os.path.abspath(path)}\\tw_report_{g[0]}_{g[1]}.svg",
        )

    def print_guilds_compare(self, guilds: list) -> None:
        
        title = Panel(Text("Territory War Report"), box=DOUBLE, padding=(1,0), style="bold blue")
        table = Table(title=title, box=DOUBLE, show_lines=True)

        guild1, guild2 = self.format_guilds_overall(guilds[0], guilds[1])

        width = len(guild1.name) if len(guild1.name) > len(guild2.name) else len(guild2.name)


        table.add_column(guild1.name, justify='center', min_width=width)
        table.add_column("VS", justify='center')
        table.add_column(guild2.name, justify='center', min_width=width)

        table.add_row(guild1.memberCount, "Members", guild2.memberCount)

        table.add_row(guild1.gp, "Galactic Power", guild2.gp)
        table.add_row(guild1.overall['characterGp'], "Character GP", guild2.overall['characterGp'])
        table.add_row(guild1.overall['shipGp'], "Ship GP", guild2.overall['shipGp'])
        table.add_row(guild1.avgGp, "Avg Galactic Power", guild2.avgGp)

        table.add_row(guild1.overall['medSkillRating'], "Skill Rating (median)", guild2.overall['medSkillRating'])
        table.add_row(guild1.overall['medCurrArenaRank'], "Arena Rank (median)", guild2.overall['medCurrArenaRank'])
        table.add_row(guild1.overall['medCurrFleetArenaRank'], "Fleet Arena Rank (median)", guild2.overall['medCurrFleetArenaRank'])

        self.console.print(table)

    def print_gls_compare(self, guilds: list) -> None:

        table = Table(box=DOUBLE, show_lines=True, header_style="bold blue")

        table.add_column('')
        for gl in guilds[0].gls.keys():
            
            gl_name = Text(guilds[0].gls[gl]['name'])
            table.add_column(gl_name, justify='center')

        gls1, gls2 = self.format_gls(guilds[0].gls, guilds[1].gls)

        gls1.insert(0, guilds[0].name)
        gls2.insert(0, guilds[1].name)

        table.add_row(*gls1)
        table.add_row(*gls2)

        self.console.print(table)

    def format_gls(self, gl1: dict, gl2: dict) -> list[list]:

        gls1 = []
        gls2 = []

        for key in gl1.keys():
            if gl1[key]['count'] == 0 and gl2[key]['count'] == 0:
                gls1.append(Text(str(gl1[key]['count']), style="dim"))
                gls2.append(Text(str(gl2[key]['count']), style="dim"))
            elif gl1[key]['count'] > gl2[key]['count']:
                gls1.append(Text(str(gl1[key]['count']), style="bold green"))
                gls2.append(Text(str(gl2[key]['count']), style="bold red"))
            elif gl2[key]['count'] > gl1[key]['count']:
                gls2.append(Text(str(gl2[key]['count']), style="bold green"))
                gls1.append(Text(str(gl1[key]['count']), style="bold red"))
            else:
                gls1.append(Text(str(gl1[key]['count'])))
                gls2.append(Text(str(gl2[key]['count'])))
        return [gls1, gls2]
   
    def format_guilds_overall(self, g1: GuildTwReport, g2: GuildTwReport):

        guild1 = GuildTwReport()
        guild2 = GuildTwReport()

        guild1.name = Text(g1.name)
        guild2.name = Text(g2.name)

        # memberCount
        guild1.memberCount = Text(str(g1.memberCount), style="bold")
        guild2.memberCount = Text(str(g2.memberCount), style="bold")

        # GP
        if g1.gp > g2.gp:
            guild1.gp = Text(format_long_number(g1.gp), style="bold green")
            guild2.gp = Text(format_long_number(g2.gp), style="bold red")
        elif g1.gp < g2.gp:
            guild2.gp = Text(format_long_number(g2.gp), style="bold green")
            guild1.gp = Text(format_long_number(g1.gp), style="bold red")
        else:
            guild1.gp = Text(format_long_number(g1.gp))
            guild2.gp = Text(format_long_number(g2.gp))

        # Avg GP
        if g1.avgGp > g2.avgGp:
            guild1.avgGp = Text(format_long_number(g1.avgGp), style="bold green")
            guild2.avgGp = Text(format_long_number(g2.avgGp), style="bold red")
        elif g1.avgGp < g2.avgGp:
            guild2.avgGp = Text(format_long_number(g2.avgGp), style="bold green")
            guild1.avgGp = Text(format_long_number(g1.avgGp), style="bold red")
        else:
            guild1.avgGp = Text(format_long_number(g1.avgGp))
            guild2.avgGp = Text(format_long_number(g2.avgGp))


        # Overall characterGp
        if g1.overall['characterGp'] > g2.overall['characterGp']:
            guild1.overall['characterGp'] = Text(format_long_number(g1.overall['characterGp']), style="bold green")
            guild2.overall['characterGp'] = Text(format_long_number(g2.overall['characterGp']), style="bold red")
        elif g1.overall['characterGp'] < g2.overall['characterGp']:
            guild2.overall['characterGp'] = Text(format_long_number(g2.overall['characterGp']), style="bold green")
            guild1.overall['characterGp'] = Text(format_long_number(g1.overall['characterGp']), style="bold red")
        else:
            guild1.overall['characterGp'] = Text(format_long_number(g1.overall['characterGp']))
            guild2.overall['characterGp'] = Text(format_long_number(g2.overall['characterGp']))
        

        # Overall shipGp
        if g1.overall['shipGp'] > g2.overall['shipGp']:
            guild1.overall['shipGp'] = Text(format_long_number(g1.overall['shipGp']), style="bold green")
            guild2.overall['shipGp'] = Text(format_long_number(g2.overall['shipGp']), style="bold red")
        elif g1.overall['shipGp'] < g2.overall['shipGp']:
            guild2.overall['shipGp'] = Text(format_long_number(g2.overall['shipGp']), style="bold green")
            guild1.overall['shipGp'] = Text(format_long_number(g1.overall['shipGp']), style="bold red")
        else:
            guild1.overall['shipGp'] = Text(format_long_number(g1.overall['shipGp']))
            guild2.overall['shipGp'] = Text(format_long_number(g2.overall['shipGp']))


        # Overall medSkillRating
        if g1.overall['medSkillRating'] > g2.overall['medSkillRating']:
            guild1.overall['medSkillRating'] = Text(format_long_number(g1.overall['medSkillRating']), style="bold green")
            guild2.overall['medSkillRating'] = Text(format_long_number(g2.overall['medSkillRating']), style="bold red")
        elif g1.overall['medSkillRating'] < g2.overall['medSkillRating']:
            guild2.overall['medSkillRating'] = Text(format_long_number(g2.overall['medSkillRating']), style="bold green")
            guild1.overall['medSkillRating'] = Text(format_long_number(g1.overall['medSkillRating']), style="bold red")
        else:
            guild1.overall['medSkillRating'] = Text(format_long_number(g1.overall['medSkillRating']))
            guild2.overall['medSkillRating'] = Text(format_long_number(g2.overall['medSkillRating']))

        # Overall medCurrArenaRank
        if g1.overall['medCurrArenaRank'] > g2.overall['medCurrArenaRank']:
            guild1.overall['medCurrArenaRank'] = Text(format_long_number(g1.overall['medCurrArenaRank']), style="bold red")
            guild2.overall['medCurrArenaRank'] = Text(format_long_number(g2.overall['medCurrArenaRank']), style="bold green")
        elif g1.overall['medCurrArenaRank'] < g2.overall['medCurrArenaRank']:
            guild2.overall['medCurrArenaRank'] = Text(format_long_number(g2.overall['medCurrArenaRank']), style="bold red")
            guild1.overall['medCurrArenaRank'] = Text(format_long_number(g1.overall['medCurrArenaRank']), style="bold green")
        else:
            guild1.overall['medCurrArenaRank'] = Text(format_long_number(g1.overall['medCurrArenaRank']))
            guild2.overall['medCurrArenaRank'] = Text(format_long_number(g2.overall['medCurrArenaRank']))

        
        # Overall medCurrFleetArenaRank
        if g1.overall['medCurrFleetArenaRank'] > g2.overall['medCurrFleetArenaRank']:
            guild1.overall['medCurrFleetArenaRank'] = Text(format_long_number(g1.overall['medCurrFleetArenaRank']), style="bold red")
            guild2.overall['medCurrFleetArenaRank'] = Text(format_long_number(g2.overall['medCurrFleetArenaRank']), style="bold green")
        elif g1.overall['medCurrFleetArenaRank'] < g2.overall['medCurrFleetArenaRank']:
            guild2.overall['medCurrFleetArenaRank'] = Text(format_long_number(g2.overall['medCurrFleetArenaRank']), style="bold red")
            guild1.overall['medCurrFleetArenaRank'] = Text(format_long_number(g1.overall['medCurrFleetArenaRank']), style="bold green")
        else:
            guild1.overall['medCurrFleetArenaRank'] = Text(format_long_number(g1.overall['medCurrFleetArenaRank']))
            guild2.overall['medCurrFleetArenaRank'] = Text(format_long_number(g2.overall['medCurrFleetArenaRank']))

        
        return [guild1, guild2]

