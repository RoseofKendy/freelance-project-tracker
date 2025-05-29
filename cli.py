# cli.py
import click
from sqlalchemy.orm import Session
from datetime import datetime
from tabulate import tabulate # For pretty tables
import csv

from database import init_db, get_db
from models import Client, Project, Task, Payment

# Initialize the database when the CLI starts
init_db()

@click.group()
def cli():
    """
    Freelance Project Tracker CLI System.
    Manage your clients, projects, tasks, and payments.
    """
    pass

# --- Client Management ---
@cli.command()
@click.option('--name', prompt='Client Name', help='Name of the client.')
@click.option('--contact', prompt='Contact Person (optional)', default='', help='Contact person at the client.')
@click.option('--email', prompt='Email (optional)', default='', help='Client email address.')
@click.option('--phone', prompt='Phone (optional)', default='', help='Client phone number.')
def add_client(name, contact, email, phone):
    """Adds a new client."""
    db: Session = next(get_db()) # Get a database session
    existing_client = db.query(Client).filter_by(name=name).first()
    if existing_client:
        click.echo(f"Error: Client '{name}' already exists.")
        return

    client = Client(name=name, contact_person=contact, email=email, phone=phone)
    db.add(client)
    db.commit()
    db.refresh(client)
    click.echo(f"Client '{client.name}' added with ID: {client.id}")
    db.close()

@cli.command()
def list_clients():
    """Lists all clients."""
    db: Session = next(get_db())
    clients = db.query(Client).all()
    if not clients:
        click.echo("No clients found.")
        return

    headers = ["ID", "Name", "Contact Person", "Email", "Phone"]
    table_data = [[c.id, c.name, c.contact_person, c.email, c.phone] for c in clients]
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
    db.close()

# --- Project Management ---
@cli.command()
@click.option('--client_id', type=int, prompt='Client ID', help='ID of the client for this project.')
@click.option('--name', prompt='Project Name', help='Name of the project.')
@click.option('--description', prompt='Description (optional)', default='', help='Brief description of the project.')
@click.option('--deadline', prompt='Deadline (YYYY-MM-DD, optional)', default='', help='Project deadline date.', callback=lambda ctx, param, value: datetime.strptime(value.split()[0], '%Y-%m-%d') if value else None)
@click.option('--priority', type=click.Choice(['Low', 'Medium', 'High']), default='', help='Priority of the project.')
def add_project(client_id, name, description, deadline, priority):
    """Adds a new project to a client."""
    db: Session = next(get_db())
    client = db.get(Client, client_id)
    if not client:
        click.echo(f"Error: Client with ID {client_id} not found.")
        return

    project = Project(
        name=name,
        description=description,
        deadline=deadline,
        priority=priority,
        client=client
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    click.echo(f"Project '{project.name}' added for client '{client.name}' with ID: {project.id}")
    db.close()

@cli.command()
@click.option('--client_id', type=int, default=None, help='Filter projects by Client ID.')
def list_projects(client_id):
    """Lists all projects, optionally filtered by client."""
    db: Session = next(get_db())
    query = db.query(Project)
    if client_id:
        query = query.filter(Project.client_id == client_id)

    projects = query.all()
    if not projects:
        click.echo("No projects found.")
        return

    headers = ["ID", "Project Name", "Client", "Deadline", "Priority", "Status", "Progress"]
    table_data = []
    for p in projects:
        progress = f"{p.get_progress_percentage():.2f}%"
        table_data.append([
            p.id, p.name, p.client.name if p.client else 'N/A',
            p.deadline.strftime('%Y-%m-%d') if p.deadline else 'N/A',
            p.priority, p.status, progress
        ])
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
    db.close()

# --- Task Tracking ---
@cli.command()
@click.option('--project_id', type=int, prompt='Project ID', help='ID of the project to add the task to.')
@click.option('--description', prompt='Task Description', help='Description of the task.')
def add_task(project_id, description):
    """Adds a new task to a project."""
    db: Session = next(get_db())
    project = db.get(Project, project_id)
    if not project:
        click.echo(f"Error: Project with ID {project_id} not found.")
        return

    task = Task(description=description, project=project)
    db.add(task)
    db.commit()
    db.refresh(task)
    click.echo(f"Task '{task.description[:50]}...' added to project '{project.name}' with ID: {task.id}")
    db.close()

@cli.command()
@click.option('--task_id', type=int, prompt='Task ID', help='ID of the task to mark as complete.')
def mark_task_complete(task_id):
    """Marks a task as complete."""
    db: Session = next(get_db())
    task = db.get(Task, task_id)
    if not task:
        click.echo(f"Error: Task with ID {task_id} not found.")
        return

    if task.is_completed:
        click.echo(f"Task '{task.description[:50]}...' (ID: {task.id}) is already marked complete.")
        return

    task.is_completed = True
    task.completed_at = datetime.now()
    db.commit()
    db.refresh(task)
    click.echo(f"Task '{task.description[:50]}...' (ID: {task.id}) marked as complete.")
    db.close()

@cli.command()
@click.option('--project_id', type=int, default=None, help='Filter progress by Project ID.')
def progress_report(project_id):
    """Views task completion percentage for each project, or a specific project."""
    db: Session = next(get_db())
    query = db.query(Project)
    if project_id:
        query = query.filter(Project.id == project_id)

    projects = query.all()
    if not projects:
        click.echo("No projects found for the given criteria.")
        return

    headers = ["Project ID", "Project Name", "Client", "Progress (%)", "Total Tasks", "Completed Tasks"]
    table_data = []
    for p in projects:
        total_tasks = len(p.tasks)
        completed_tasks = sum(1 for task in p.tasks if task.is_completed)
        progress = p.get_progress_percentage()
        table_data.append([
            p.id,
            p.name,
            p.client.name if p.client else 'N/A',
            f"{progress:.2f}",
            total_tasks,
            completed_tasks
        ])
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
    db.close()

# --- Payment Logging ---
@cli.command()
@click.option('--project_id', type=int, prompt='Project ID', help='ID of the project for this payment.')
@click.option('--amount', type=float, prompt='Amount', help='Amount of the payment.')
@click.option('--type', 'payment_type', type=click.Choice(['Invoice', 'Received', 'Pending']), prompt='Payment Type', help='Type of payment (Invoice, Received, Pending).')
@click.option('--notes', prompt='Notes (optional)', default='', help='Any additional notes for the payment.')
def log_payment(project_id, amount, payment_type, notes):
    """Records a new payment for a project."""
    db: Session = next(get_db())
    project = db.get(Project, project_id)
    if not project:
        click.echo(f"Error: Project with ID {project_id} not found.")
        return

    payment = Payment(
        project_id=project_id,
        amount=amount,
        payment_type=payment_type,
        notes=notes
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    click.echo(f"Payment of ${payment.amount:.2f} ({payment.payment_type}) logged for project '{project.name}' with ID: {payment.id}")
    db.close()

@cli.command()
@click.option('--project_id', type=int, default=None, help='Filter payments by Project ID.')
def view_payments(project_id):
    """Views all payments, grouped by project or for a specific project."""
    db: Session = next(get_db())
    query = db.query(Payment)
    if project_id:
        query = query.filter(Payment.project_id == project_id)

    payments = query.all()
    if not payments:
        click.echo("No payments found.")
        return

    headers = ["ID", "Project Name", "Amount", "Type", "Date", "Notes"]
    table_data = []
    for p in payments:
        table_data.append([
            p.id,
            p.project.name if p.project else 'N/A',
            f"${p.amount:.2f}",
            p.payment_type,
            p.date.strftime('%Y-%m-%d %H:%M:%S'),
            p.notes
        ])
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
    db.close()

# --- Advanced Features ---
@cli.command()
@click.option('--output_file', default='freelance_data.csv', help='Name of the CSV file to export to.')
def export_to_csv(output_file):
    """Exports all client, project, task, and payment data to a CSV file."""
    db: Session = next(get_db())
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Clients
            writer.writerow(["--- Clients ---"])
            writer.writerow(["ID", "Name", "Contact Person", "Email", "Phone"])
            clients = db.query(Client).all()
            for c in clients:
                writer.writerow([c.id, c.name, c.contact_person, c.email, c.phone])
            writer.writerow([]) # Blank line for separation

            # Projects
            writer.writerow(["--- Projects ---"])
            writer.writerow(["ID", "Project Name", "Client Name", "Description", "Deadline", "Priority", "Status", "Progress (%)"])
            projects = db.query(Project).all()
            for p in projects:
                progress = f"{p.get_progress_percentage():.2f}"
                writer.writerow([
                    p.id, p.name, p.client.name if p.client else 'N/A',
                    p.description, p.deadline.strftime('%Y-%m-%d') if p.deadline else 'N/A',
                    p.priority, p.status, progress
                ])
            writer.writerow([])

            # Tasks
            writer.writerow(["--- Tasks ---"])
            writer.writerow(["ID", "Project Name", "Description", "Completed", "Created At", "Completed At"])
            tasks = db.query(Task).all()
            for t in tasks:
                writer.writerow([
                    t.id, t.project.name if t.project else 'N/A', t.description,
                    "Yes" if t.is_completed else "No",
                    t.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    t.completed_at.strftime('%Y-%m-%d %H:%M:%S') if t.completed_at else 'N/A'
                ])
            writer.writerow([])

            # Payments
            writer.writerow(["--- Payments ---"])
            writer.writerow(["ID", "Project Name", "Amount", "Type", "Date", "Notes"])
            payments = db.query(Payment).all()
            for p in payments:
                writer.writerow([
                    p.id, p.project.name if p.project else 'N/A', f"{p.amount:.2f}",
                    p.payment_type, p.date.strftime('%Y-%m-%d %H:%M:%S'), p.notes
                ])
        click.echo(f"All data exported successfully to '{output_file}'")
    except Exception as e:
        click.echo(f"Error exporting data: {e}")
    finally:
        db.close()

@cli.command()
@click.option('--query_string', prompt='Search term', help='Term to search for in client/project/task/payment names/descriptions/notes.')
def search(query_string):
    """Searches for the given term across clients, projects, tasks, and payments."""
    db: Session = next(get_db())
    search_term = f"%{query_string}%"

    click.echo(f"\n--- Search Results for '{query_string}' ---\n")

    # Search Clients
    clients = db.query(Client).filter(
        (Client.name.like(search_term)) |
        (Client.contact_person.like(search_term)) |
        (Client.email.like(search_term)) |
        (Client.phone.like(search_term))
    ).all()
    if clients:
        click.echo("Clients Found:")
        headers = ["ID", "Name", "Contact Person", "Email", "Phone"]
        table_data = [[c.id, c.name, c.contact_person, c.email, c.phone] for c in clients]
        click.echo(tabulate(table_data, headers=headers, tablefmt="plain"))
    else:
        click.echo("No clients found matching the search term.")
    click.echo("-" * 40)

    # Search Projects
    projects = db.query(Project).filter(
        (Project.name.like(search_term)) |
        (Project.description.like(search_term))
    ).all()
    if projects:
        click.echo("Projects Found:")
        headers = ["ID", "Project Name", "Client", "Description"]
        table_data = [[p.id, p.name, p.client.name if p.client else 'N/A', p.description[:50] + '...' if len(p.description) > 50 else p.description] for p in projects]
        click.echo(tabulate(table_data, headers=headers, tablefmt="plain"))
    else:
        click.echo("No projects found matching the search term.")
    click.echo("-" * 40)

    # Search Tasks
    tasks = db.query(Task).filter(Task.description.like(search_term)).all()
    if tasks:
        click.echo("Tasks Found:")
        headers = ["ID", "Project Name", "Description", "Completed"]
        table_data = [[t.id, t.project.name if t.project else 'N/A', t.description[:50] + '...' if len(t.description) > 50 else t.description, "Yes" if t.is_completed else "No"] for t in tasks]
        click.echo(tabulate(table_data, headers=headers, tablefmt="plain"))
    else:
        click.echo("No tasks found matching the search term.")
    click.echo("-" * 40)

    # Search Payments
    payments = db.query(Payment).filter(Payment.notes.like(search_term)).all()
    if payments:
        click.echo("Payments Found:")
        headers = ["ID", "Project Name", "Amount", "Type", "Notes"]
        table_data = [[p.id, p.project.name if p.project else 'N/A', f"${p.amount:.2f}", p.payment_type, p.notes[:50] + '...' if len(p.notes) > 50 else p.notes] for p in payments]
        click.echo(tabulate(table_data, headers=headers, tablefmt="plain"))
    else:
        click.echo("No payments found matching the search term.")
    click.echo("-" * 40)

    db.close()


if __name__ == '__main__':
    cli()
