import click
from swgoh.classes import GuildManager, Printer


@click.group()
@click.option('--home', envvar='GUILD_ID', default='')
@click.pass_context
def guild(ctx, home):
    ctx.obj = { 'guild_id':  home }
    


@guild.command()
@click.argument('guilds_to_compare', required=True, type=str, nargs=-1)
@click.option('--force', is_flag=True)
@click.pass_obj
def compare(obj, guilds_to_compare, force):
    
    guild_manager = GuildManager()
    guilds_to_compare = list(guilds_to_compare)

    if len(guilds_to_compare) < 1:
        click.echo("Guild id/s missing.... ")
        return
    
    if len(guilds_to_compare) == 1:
        # TODO: Check if default guild is set in ctx.obj
        guilds_to_compare.insert(0, obj['guild_id'])
    
    result = guild_manager.compare(guilds_to_compare, force)
    
    if len(result) < 2:
        click.echo("Not all guilds are found!")
    
    printer = Printer()
    printer.print_guilds_compare(result)

    # for guild in result:
    #     if guild:
    #         click.secho(guild.name, bold=True, fg='green')
    #         click.secho(guild.gp)
    #         click.secho(guild.overall)
    #     else: 
    #         click.echo("Guild not found")

    
    



