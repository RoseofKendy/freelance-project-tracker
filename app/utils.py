from datetime import datetime
from app.database import Session
from app.models import Client, Project, Task, Payment


# -------------------------------
# CLIENT MANAGEMENT
# -------------------------------

def add_client(name):
    session = Session()
    if session.query(Client).filter_by(name=name).first():
        print(f"Client '{name}' already exists.")
        return
    client = Client(name=name)
    session.add(client)
    session.commit()
    print(f"✅ Client '{name}' added.")


def list_clients():
    session = Session()
    clients = session.query(Client).all()
    if not clients:
        print("No clients found.")
        return
    print("📋 Clients:")
    for client in clients:
        print(f"  - {client.name}")


# -------------------------------
# PROJECT MANAGEMENT
# -------------------------------

def add_project(title, client_name, priority, deadline):
    session = Session()
    client = session.query(Client).filter_by(name=client_name).first()
    if not client:
        print(f"❌ Client '{client_name}' not found.")
        return
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else None
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return
    project = Project(title=title, priority=priority, deadline=deadline_date, client=client)
    session.add(project)
    session.commit()
    print(f"✅ Project '{title}' added under client '{client_name}'.")


def list_projects():
    session = Session()
    projects = session.query(Project).all()
    if not projects:
        print("No projects found.")
        return
    print("📋 Projects:")
    for project in projects:
        deadline = project.deadline.strftime('%Y-%m-%d') if project.deadline else "None"
        print(f"  [{project.id}] {project.title} (Client: {project.client.name}, Priority: {project.priority}, Deadline: {deadline})")


# -------------------------------
# TASK MANAGEMENT
# -------------------------------

def add_task(project_title, description):
    session = Session()
    project = session.query(Project).filter_by(title=project_title).first()
    if not project:
        print(f"❌ Project '{project_title}' not found.")
        return
    task = Task(description=description, complete=False, project=project)
    session.add(task)
    session.commit()
    print(f"✅ Task added to project '{project_title}'.")


def mark_task_complete(task_id):
    session = Session()
    task = session.query(Task).get(task_id)
    if not task:
        print(f"❌ Task with ID {task_id} not found.")
        return
    if task.complete:
        print(f"ℹ️ Task [{task.id}] is already marked as complete.")
        return
    task.complete = True
    session.commit()
    print(f"✅ Task [{task.id}] marked as complete.")


def task_progress_report():
    session = Session()
    projects = session.query(Project).all()
    if not projects:
        print("No projects found.")
        return
    print("📊 Task Progress:")
    for project in projects:
        total_tasks = len(project.tasks)
        completed = len([t for t in project.tasks if t.complete])
        percent = (completed / total_tasks) * 100 if total_tasks > 0 else 0
        print(f"  - {project.title}: {completed}/{total_tasks} tasks complete ({percent:.0f}%)")


# -------------------------------
# PAYMENT LOGGING
# -------------------------------

def log_payment(project_title, amount, status, date=None):
    session = Session()
    project = session.query(Project).filter_by(title=project_title).first()
    if not project:
        print(f"❌ Project '{project_title}' not found.")
        return
    try:
        payment_date = datetime.strptime(date, "%Y-%m-%d").date() if date else datetime.today().date()
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return
    payment = Payment(amount=amount, status=status, date=payment_date, project=project)
    session.add(payment)
    session.commit()
    print(f"✅ Payment of {amount:.2f} ({status}) logged for project '{project_title}' on {payment_date}.")


def view_payments():
    session = Session()
    projects = session.query(Project).all()
    if not projects:
        print("No projects found.")
        return
    print("💰 Payment Logs:")
    for project in projects:
        print(f"\n🔹 Project: {project.title}")
        if not project.payments:
            print("  No payments logged.")
            continue
        for payment in project.payments:
            print(f"  [{payment.id}] {payment.date} - {payment.amount:.2f} ({payment.status.title()})")
