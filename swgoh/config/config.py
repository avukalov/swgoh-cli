import asyncclick as click



@click.group()
#@click.option('--home', envvar='GUILD_ID', default='')
@click.pass_context
def config(ctx):
    # ctx.obj = { 'home_guild_id':  home }
    pass



@config.command()
@click.pass_context
def test(ctx):
    print("config test!")