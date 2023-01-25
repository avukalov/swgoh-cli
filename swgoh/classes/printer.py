import json
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel


class Printer:
    def __init__(self) -> None:
        self.console = Console()
        

    def print_guilds_compare(self, guilds: list) -> None:

        table = Table(
            title="Territory War Comparsion",
            show_lines=True
        )

        guild_1 = guilds[0]
        guild_2 = guilds[1]

        self.format_guilds(guild_1, guild_2)

        table.add_column(guild_1.name, justify='right', min_width=25)
        table.add_column("vs", justify='center')
        table.add_column(guild_2.name, justify='left', min_width=25)

        table.add_row(guild_1.memberCount, "Members", guild_2.memberCount)

        table.add_row(guild_1.gp, "Galactic Power", guild_2.gp)
        table.add_row(guild_1.overall['characterGp'], "Character GP", guild_2.overall['characterGp'])
        table.add_row(guild_1.overall['shipGp'], "Ship GP", guild_2.overall['shipGp'])
        table.add_row(guild_1.avgGp, "Avg Galactic Power", guild_2.avgGp)

        table.add_row(guild_1.overall['medSkillRating'], "Skill Rating (median)", guild_2.overall['medSkillRating'])
        table.add_row(guild_1.overall['medCurrArenaRank'], "Arena Rank (median)", guild_2.overall['medCurrArenaRank'])
        table.add_row(guild_1.overall['medCurrFleetArenaRank'], "Fleet Arena Rank (median)", guild_2.overall['medCurrFleetArenaRank'])

        self.console.print(table)

    def print_gls_compare(self, guilds: list) -> None:

        table = Table(
            show_lines=True,
            padding=(0,2),
        )

        table.add_column('')
        for gl in guilds[0].gls.keys():
            table.add_column(guilds[0].gls[gl]['name'], justify='center')

        for guild in guilds:
            table.add_row(
                f'[bold]{guild.name}[/bold]',
                str(guild.gls['JABBATHEHUTT']['count']),
                str(guild.gls['JEDIMASTERKENOBI']['count']),
                str(guild.gls['JEDIMASTERLUKSKYWALKER']['count']),
                str(guild.gls['LORDVADER']['count']),
                str(guild.gls['GLREY']['count']),
                str(guild.gls['SITHETERNALEMPEROR']['count']),
                str(guild.gls['SUPREMELEADERKYLOREN']['count'])
            )
            
            #self.console.print_json(json.dumps(guild.__dict__))
            # gls_panels = [self.format_gls(guild.gls[key]) for key in guild.gls.keys()]
            # columns = Columns(gls_panels, title=guild.name, padding=(10, 5))
            # self.console.print(columns)

        self.console.print(table)

    def format_gls(self, gl: dict) -> str:
        return f"[bold]{gl['name']}[/bold]\n[bold]{gl['count']}[/bold]"
        
    def format_guilds(self, g1, g2):

        g1.memberCount = f"[b]{g1.memberCount}[/b]"
        g2.memberCount = f"[b]{g2.memberCount}[/b]"
        
        # GP
        if g1.gp > g2.gp:
            g1.gp = "[b][green]{:,}[/b]".format(g1.gp)
            g2.gp = "[red]{:,}".format(g2.gp)
        elif g1.gp < g2.gp:
            g1.gp = "[red]{:,}".format(g1.gp)
            g2.gp = "[b][green]{:,}[/b]".format(g2.gp)
        else:
            g1.gp = "[b]{:,}[/b]".format(g1.gp)
            g2.gp = "[b]{:,}[/b]".format(g2.gp)

        # Avg GP
        if g1.avgGp > g2.avgGp:
            g1.avgGp = "[b][green]{:,}[/b]".format(g1.avgGp)
            g2.avgGp = "[red]{:,}".format(g2.avgGp)
        elif g1.avgGp < g2.avgGp:
            g1.avgGp = "[red]{:,}".format(g1.avgGp)
            g2.avgGp = "[b][green]{:,}[/b]".format(g2.avgGp)
        else:
            g1.avgGp = "[b]{:,}[/b]".format(g1.avgGp)
            g2.avgGp = "[b]{:,}[/b]".format(g2.avgGp)


        # Overall characterGp
        if g1.overall['characterGp'] > g2.overall['characterGp']:
            g1.overall['characterGp'] = "[b][green]{:,}[/b]".format(g1.overall['characterGp'])
            g2.overall['characterGp'] = "[red]{:,}".format(g2.overall['characterGp'])
        elif g1.overall['characterGp'] < g2.overall['characterGp']:
            g1.overall['characterGp'] = "[red]{:,}".format(g1.overall['characterGp'])
            g2.overall['characterGp'] = "[b][green]{:,}[/b]".format(g2.overall['characterGp'])
        else:
            g1.overall['characterGp'] = "[b]{:,}[/b]".format(g1.overall['characterGp'])
            g2.overall['characterGp'] = "[b]{:,}[/b]".format(g2.overall['characterGp'])

        
        # Overall shipGp
        if g1.overall['shipGp'] > g2.overall['shipGp']:
            g1.overall['shipGp'] = "[b][green]{:,}[/b]".format(g1.overall['shipGp'])
            g2.overall['shipGp'] = "[red]{:,}".format(g2.overall['shipGp'])
        elif g1.overall['shipGp'] < g2.overall['shipGp']:
            g1.overall['shipGp'] = "[red]{:,}".format(g1.overall['shipGp'])
            g2.overall['shipGp'] = "[b][green]{:,}[/b]".format(g2.overall['shipGp'])
        else:
            g1.overall['shipGp'] = "[b]{:,}[/b]".format(g1.overall['shipGp'])
            g2.overall['shipGp'] = "[b]{:,}[/b]".format(g2.overall['shipGp'])

        # Overall medSkillRating
        if g1.overall['medSkillRating'] > g2.overall['medSkillRating']:
            g1.overall['medSkillRating'] = "[b][green]{:,}[/b]".format(g1.overall['medSkillRating'])
            g2.overall['medSkillRating'] = "[red]{:,}".format(g2.overall['medSkillRating'])
        elif g1.overall['medSkillRating'] < g2.overall['medSkillRating']:
            g1.overall['medSkillRating'] = "[red]{:,}".format(g1.overall['medSkillRating'])
            g2.overall['medSkillRating'] = "[b][green]{:,}[/b]".format(g2.overall['medSkillRating'])
        else:
            g1.overall['medSkillRating'] = "[b]{:,}[/b]".format(g1.overall['medSkillRating'])
            g2.overall['medSkillRating'] = "[b]{:,}[/b]".format(g2.overall['medSkillRating'])

        # Overall medCurrArenaRank
        if g1.overall['medCurrArenaRank'] < g2.overall['medCurrArenaRank']:
            g1.overall['medCurrArenaRank'] = "[b][green]{:,}[/b]".format(g1.overall['medCurrArenaRank'])
            g2.overall['medCurrArenaRank'] = "[red]{:,}".format(g2.overall['medCurrArenaRank'])
        elif g1.overall['medCurrArenaRank'] > g2.overall['medCurrArenaRank']:
            g1.overall['medCurrArenaRank'] = "[red]{:,}".format(g1.overall['medCurrArenaRank'])
            g2.overall['medCurrArenaRank'] = "[b][green]{:,}[/b]".format(g2.overall['medCurrArenaRank'])
        else:
            g1.overall['medCurrArenaRank'] = "[b]{:,}[/b]".format(g1.overall['medCurrArenaRank'])
            g2.overall['medCurrArenaRank'] = "[b]{:,}[/b]".format(g2.overall['medCurrArenaRank'])
        
        # Overall medCurrFleetArenaRank
        if g1.overall['medCurrFleetArenaRank'] < g2.overall['medCurrFleetArenaRank']:
            g1.overall['medCurrFleetArenaRank'] = "[b][green]{:,}[/b]".format(g1.overall['medCurrFleetArenaRank'])
            g2.overall['medCurrFleetArenaRank'] = "[red]{:,}".format(g2.overall['medCurrFleetArenaRank'])
        elif g1.overall['medCurrFleetArenaRank'] > g2.overall['medCurrFleetArenaRank']:
            g1.overall['medCurrFleetArenaRank'] = "[red]{:,}".format(g1.overall['medCurrFleetArenaRank'])
            g2.overall['medCurrFleetArenaRank'] = "[b][green]{:,}[/b]".format(g2.overall['medCurrFleetArenaRank'])
        else:
            g1.overall['medCurrFleetArenaRank'] = "[b]{:,}[/b]".format(g1.overall['medCurrFleetArenaRank'])
            g2.overall['medCurrFleetArenaRank'] = "[b]{:,}[/b]".format(g2.overall['medCurrFleetArenaRank'])
