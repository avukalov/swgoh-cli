import os, click, json
from typing import Tuple
from swgoh import console
from swgoh.services import GuildService, Printer



@click.group()
@click.option('--home', envvar='GUILD_ID', default='')
@click.pass_context
def guild(ctx, home):
    ctx.obj = { 'my_guild_id':  home }
    


@guild.command()
@click.argument('ids', required=True, type=str, nargs=-1)
@click.option('--sync', is_flag=True, help="Calls api to get most recent data even if data cached")
@click.option('--export', type=str, default=None, help="Exports print output in SVG format to given path")
@click.pass_context
def compare(ctx, ids, sync, export):
    
    # console.print(type(ids))
    # return 
    ids = validate_compare_input(ctx.obj, ids)
    if not ids:
        console.print("Execute: swgoh guild compare --help to show more info.")
        return

    result = GuildService().compare(ids, sync)
    
    if len(result) < 2:
        console.print("Not all guilds are found!")
    
    printer = Printer()
    printer.print_guilds_compare(result)
    printer.print_gls_compare(result)

    # console.print(os.path.abspath(export))
    if export:
        printer.export_svg(export, [guild.name for guild in result])


def validate_compare_input(obj: dict, ids: Tuple[str, str]) -> Tuple[str, str] | None:
    
    if len(ids) > 2:
        return (ids[0], ids[1])
    
    if len(ids) == 1:
        my_guild = obj['my_guild_id']
        if not my_guild:
            return None
        ids = (obj['my_guild_id'], ids[0])

    return ids



    
    



