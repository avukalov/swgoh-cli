import asyncclick as click
from dotenv import load_dotenv

from swgoh.guild import guild_group
from swgoh.config import config_group

@click.group()
@click.pass_context
async def cli(ctx):
    """Swgoh cli is a helper tool for game Star Wars Galaxy of Heroes. """
    
    ctx.obj = {}
    load_dotenv()
    
    #cache.load_initial_cache();



cli.add_command(guild_group)
cli.add_command(config_group)


#TB_HOTH_IMPERIAL_RETALIATION
#"profession_bountyhunter"
#"affiliation_imperialtrooper"