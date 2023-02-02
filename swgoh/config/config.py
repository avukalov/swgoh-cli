import asyncclick as click
from swgoh.shared import ComlinkSyncService


@click.group()
#@click.option('--home', envvar='GUILD_ID', default='')
@click.pass_context
async def config(ctx):
    # ctx.obj = { 'homeGuildId':  home }
    pass



@config.command()
@click.option('--sync', is_flag=True, help="Calls api to get most recent data even if data cached")
@click.pass_context
async def test(ctx, sync):
    comlink = await ComlinkSyncService()
    await comlink.getGuild2(ctx.obj['homeGuildId'], sync)
    print("config test!")