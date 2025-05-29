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
    client = db.query(Client).get(client_id)
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
    project = db.query(Project).get(project_id)
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
    """
    Marks a task as complete and automatically updates the project status
    to 'Completed' if all tasks in that project are complete.
    """
    db: Session = next(get_db())
    task = db.query(Task).get(task_id)
    if not task:
        click.echo(f"Error: Task with ID {task_id} not found.")
        return

    if task.is_completed:
        click.echo(f"Task '{task.description[:50]}...' (ID: {task.id}) is already marked complete.")
        db.close()
        return

    task.is_completed = True
    task.completed_at = datetime.now()
    db.commit()
    db.refresh(task) # Refresh to ensure relationship is loaded if not already
    click.echo(f"Task '{task.description[:50]}...' (ID: {task.id}) marked as complete.")

    # --- NEW LOGIC FOR AUTOMATIC PROJECT COMPLETION ---
    project = task.project # Get the project associated with this task
    if project:
        # Check if all tasks for this project are completed
        all_tasks_completed = all(t.is_completed for t in project.tasks)

        if all_tasks_completed and project.status != 'Completed':
            project.status = 'Completed'
            db.commit()
            db.refresh(project)
            click.echo(f"Project '{project.name}' (ID: {project.id}) status automatically updated to 'Completed' as all tasks are done!")
        elif not all_tasks_completed and project.status == 'Completed':
            # This handles a theoretical edge case where a task might be marked incomplete
            # after a project was completed, though our current CLI doesn't allow un-completing.
            # It's good practice to consider.
            project.status = 'In Progress' # Or 'Pending' depending on desired logic
            db.commit()
            db.refresh(project)
            click.echo(f"Project '{project.name}' (ID: {project.id}) status reverted to '{project.status}' as not all tasks are complete.")
    # --- END NEW LOGIC ---

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
    project = db.query(Project).get(project_id)
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

# --- Comprehensive Report ---
@cli.command()
def comprehensive_report():
    """
    Generates a comprehensive report of all clients, projects, tasks, and payments.
    Presents information grouped by client and project for readability.
    """
    db: Session = next(get_db())
    clients = db.query(Client).order_by(Client.name).all()

    if not clients:
        click.echo("No data found in the system.")
        db.close()
        return

    click.echo("\n" + "="*80)
    click.echo("                     COMPREHENSIVE FREELANCE PROJECT REPORT")
    click.echo("="*80 + "\n")

    for client in clients:
        click.echo(f"\n--- CLIENT: {client.name} (ID: {client.id}) ---")
        client_details = [
            ["Contact Person", client.contact_person or "N/A"],
            ["Email", client.email or "N/A"],
            ["Phone", client.phone or "N/A"]
        ]
        click.echo(tabulate(client_details, tablefmt="plain"))

        projects = client.projects
        if not projects:
            click.echo("  No projects for this client.")
            continue

        click.echo("\n  PROJECTS:")
        project_headers = ["Project ID", "Name", "Deadline", "Priority", "Status", "Progress (%)"]
        project_data = []
        for project in projects:
            progress = f"{project.get_progress_percentage():.2f}"
            project_data.append([
                project.id,
                project.name,
                project.deadline.strftime('%Y-%m-%d') if project.deadline else 'N/A',
                project.priority,
                project.status,
                progress
            ])
        click.echo(tabulate(project_data, headers=project_headers, tablefmt="grid", numalign="left"))

        for project in projects:
            click.echo(f"\n    Tasks for Project '{project.name}' (ID: {project.id}):")
            tasks = project.tasks
            if not tasks:
                click.echo("      No tasks for this project.")
            else:
                task_headers = ["Task ID", "Description", "Completed", "Created At"]
                task_data = []
                for task in tasks:
                    task_data.append([
                        task.id,
                        task.description[:60] + "..." if len(task.description) > 60 else task.description,
                        "Yes" if task.is_completed else "No",
                        task.created_at.strftime('%Y-%m-%d')
                    ])
                click.echo(tabulate(task_data, headers=task_headers, tablefmt="plain", numalign="left"))

            click.echo(f"\n    Payments for Project '{project.name}' (ID: {project.id}):")
            payments = project.payments
            if not payments:
                click.echo("      No payments for this project.")
            else:
                payment_headers = ["Payment ID", "Amount", "Type", "Date", "Notes"]
                payment_data = []
                for payment in payments:
                    payment_data.append([
                        payment.id,
                        f"${payment.amount:.2f}",
                        payment.payment_type,
                        payment.date.strftime('%Y-%m-%d'),
                        payment.notes[:60] + "..." if len(payment.notes) > 60 else payment.notes
                    ])
                click.echo(tabulate(payment_data, headers=payment_headers, tablefmt="plain", numalign="left"))
        click.echo("\n" + "-"*80) # Separator between clients

    db.close()
    click.echo("\n" + "="*80)
    click.echo("                         REPORT ENDS")
    click.echo("="*80 + "\n")


if __name__ == '__main__':
    cli()
