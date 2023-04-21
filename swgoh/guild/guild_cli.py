import os, json, datetime
import asyncclick as click
from typing import Tuple
from swgoh import console
from swgoh.config import config, config_group
from swgoh.guild.guild_manager import GuildManager
from swgoh.guild.printer import Printer



@click.group()
@click.option('--set-home', type=str, required=False, help="Saves home guild id for further use ")
@click.pass_context
async def guild(ctx, set_home):
    if set_home:
        os.environ['GUILD_ID'] = set_home
        ctx.obj['homeGuildId'] = set_home
    ctx.obj['homeGuildId'] = os.getenv('GUILD_ID')


# DEBUG
guild.add_command(config_group)


@guild.command()
@click.argument('ids', required=True, type=str, nargs=-1)
@click.option('--sync', is_flag=True, help="Calls api to get most recent data even if data cached")
@click.option('--export', type=str, default=None, help="Exports print output in SVG format to given path")
@click.pass_context
async def compare(ctx, ids, sync, export):
    
    gm = await GuildManager()
    ids = validate_compare_input(ctx.obj, ids)
    if not ids:
        console.print("Execute: swgoh guild compare --help to show more info.")
        return

    result = await gm.compare(ids, sync)
    
    if len(result) < 2:
        console.print("Not all guilds are found!")
    
    # TODO: Improve printer
    printer = Printer()
    printer.print_guilds_compare(result)
    printer.print_gls_compare(result)

    if export:
        printer.export_svg(export, [guild.name for guild in result])



#
# TERRITORY BATTLES SECTION
#
#
@click.group()
@click.pass_context
async def tb(ctx):
    pass


@tb.command()
@click.option('--export', type=str, default=None, help="Exports print output in SVG format to given path")
@click.pass_context
async def dshoth(ctx, export):
    guild_id = ctx.obj['homeGuildId']
    result = GuildManager().get_hoth_requirements(guild_id)


    
    printer = Printer()
    printer.print_tb_req(result)
    if export:
        console.save_svg(
            title=f"TB DS HOTH Report - ({len(result)} records) - {datetime.datetime.now().date()}",
            path=f"{os.path.abspath(export)}.svg",
        )
    
    #console.print_json(json.dumps(result[0][0].__dict__))



@tb.command()
@click.pass_context
async def test(ctx):
    guild_id = ctx.obj['homeGuildId']
    # result = GuildManager().get_hoth_requirements(guild_id)
    console.print_json(json.dumps(config))



guild.add_command(tb)
guild.add_command(dshoth)


def validate_compare_input(obj: dict, ids: Tuple[str, str]) -> Tuple[str, str] | None:
    
    if len(ids) > 2:
        return (ids[0], ids[1])
    
    if len(ids) == 1:
        my_guild = obj['homeGuildId']
        if not my_guild:
            return None
        ids = (obj['homeGuildId'], ids[0])

    return ids



    
    



