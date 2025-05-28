import click
from app.utils import *

@click.group()
def cli():
    pass

@cli.command()
@click.argument("name")
def addclient(name):
    add_client(name)

@cli.command()
def listclients():
    list_clients()

@cli.command()
@click.argument("title")
@click.argument("client")
@click.option("--priority", default="Medium")
@click.option("--deadline", default=None)
def addproject(title, client, priority, deadline):
    add_project(title, client, priority, deadline)

@cli.command()
def listprojects():
    list_projects()

@cli.command()
@click.argument("project")
@click.argument("description")
def addtask(project, description):
    add_task(project, description)

@cli.command()
@click.argument("task_id", type=int)
def marktaskcomplete(task_id):
    mark_task_complete(task_id)

@cli.command()
def progressreport():
    task_progress_report()

@cli.command()
@click.argument("project")
@click.argument("amount", type=float)
@click.argument("status")
@click.option("--date", default=None)
def logpayment(project, amount, status, date):
    log_payment(project, amount, status, date)

@cli.command()
def viewpayments():
    view_payments()

@cli.command()
@click.argument("filename")
def exportpayments(filename):
    export_payments_csv(filename)