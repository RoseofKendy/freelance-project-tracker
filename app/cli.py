import click
from app.utils import (
    add_client, list_clients,
    add_project, list_projects,
    add_task, mark_task_complete, task_progress_report,
    log_payment, view_payments
)

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

@cli.command()
@click.argument('title')
@click.argument('client_name')
@click.option('--priority', default='Medium')
@click.option('--deadline', default=None, help='Deadline (YYYY-MM-DD)')
def addproject(title, client_name, priority, deadline):
    add_project(title, client_name, priority, deadline)

@cli.command()
def listprojects():
    list_projects()

@cli.command()
@click.argument('project_title')
@click.argument('description')
def addtask(project_title, description):
    add_task(project_title, description)

@cli.command()
@click.argument('task_id', type=int)
def marktaskcomplete(task_id):
    mark_task_complete(task_id)

@cli.command()
def progressreport():
    task_progress_report()

@cli.command()
@click.argument('project_title')
@click.argument('amount', type=float)
@click.argument('status')
@click.option('--date', default=None, help='Payment date (YYYY-MM-DD)')
def logpayment(project_title, amount, status, date):
    log_payment(project_title, amount, status, date)

@cli.command()
def viewpayments():
    view_payments()
