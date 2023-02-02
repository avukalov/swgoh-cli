import asyncclick as click
from swgoh.shared import ComlinkSyncService


@click.group()
#@click.option('--home', envvar='GUILD_ID', default='')
@click.pass_context
async def config(ctx):
    # ctx.obj = { 'homeGuildId':  home }
    pass



@config.command()
@click.pass_context
async def test(ctx):
    comlink = await ComlinkSyncService()
    await comlink.getGuild2(ctx.obj['homeGuildId'], False)
    print("config test!")