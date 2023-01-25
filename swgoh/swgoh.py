import click
from dotenv import load_dotenv

from swgoh.commands import guild 

@click.group()
@click.pass_context
def cli(ctx):
    """Swgoh cli is a helper tool for game Star Wars Galaxy of Heroes. """
    
    load_dotenv();
    #cache.load_initial_cache();



cli.add_command(guild)


