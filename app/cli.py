import click
from app.utils import *
from app.models import Task, TimeLog, Client, Project
from app.database import Session
from datetime import datetime

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
@click.option("--is_recurring", is_flag=True, help="Set if the project is recurring")
@click.option("--recurrence_interval", default=None, help="Interval: daily, weekly, monthly, etc.")
def addproject(title, client, priority, deadline, is_recurring, recurrence_interval):
    session = Session()
    client_obj = session.query(Client).get(client)
    if not client_obj:
        click.echo(f"Client with ID {client} does not exist.")
        return

    new_project = Project(
        title=title,
        client_id=client_obj.id,
        priority=priority,
        deadline=deadline,
        is_recurring=is_recurring,
        recurrence_interval=recurrence_interval if is_recurring else None
    )
    session.add(new_project)
    session.commit()
    click.echo(f"Added project '{title}' for client '{client_obj.name}' with ID {new_project.id}.")

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

@cli.command()
@click.argument('task_id', type=int)
def starttimer(task_id):
    """Start a timer for a task."""
    session = Session()
    task = session.query(Task).get(task_id)
    if not task:
        click.echo("Task not found.")
        return
    log = TimeLog(task=task)
    session.add(log)
    session.commit()
    click.echo(f"⏱️ Timer started for Task ID {task_id} at {log.start_time}.")

@cli.command()
@click.argument('task_id', type=int)
def stoptimer(task_id):
    """Stop the latest timer for a task."""
    session = Session()
    task = session.query(Task).get(task_id)
    if not task:
        click.echo("Task not found.")
        return
    log = session.query(TimeLog).filter_by(task_id=task_id, end_time=None).order_by(TimeLog.start_time.desc()).first()
    if not log:
        click.echo("No active timer found for this task.")
        return
    log.end_time = datetime.utcnow()
    session.commit()
    duration = log.duration_minutes()
    click.echo(f"✅ Timer stopped. Duration: {duration} minutes.")
