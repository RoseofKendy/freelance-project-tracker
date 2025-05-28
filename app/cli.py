import click
from app.utils import add_client, list_clients  # to be implemented

@click.group()
def cli():
    pass

@cli.command()
@click.argument('name')
def addclient(name):
    add_client(name)

@cli.command()
def listclients():
    list_clients()
