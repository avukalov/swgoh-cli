import click
from dotenv import load_dotenv

from swgoh.commands import guild, config

@click.group()
@click.pass_context
def cli(ctx):
    """Swgoh cli is a helper tool for game Star Wars Galaxy of Heroes. """
    
    ctx.obj = {}
    load_dotenv()
    #cache.load_initial_cache();



cli.add_command(guild)
cli.add_command(config)


#TB_HOTH_IMPERIAL_RETALIATION
#"profession_bountyhunter"
#"affiliation_imperialtrooper"
