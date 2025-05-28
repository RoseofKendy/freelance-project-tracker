from datetime import datetime
from app.database import Session
from app.models import Client, Project, Task, Payment
import csv

def add_client(name):
    session = Session()
    if session.query(Client).filter_by(name=name).first():
        print(f"Client '{name}' already exists.")
        return
    session.add(Client(name=name))
    session.commit()
    print(f"✅ Client '{name}' added.")

def list_clients():
    session = Session()
    clients = session.query(Client).all()
    for c in clients:
        print(f"- {c.name}")

def add_project(title, client_name, priority, deadline):
    session = Session()
    client = session.query(Client).filter_by(name=client_name).first()
    if not client:
        print(f"❌ Client '{client_name}' not found.")
        return
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date() if deadline else None
    project = Project(title=title, priority=priority, deadline=deadline_date, client=client)
    session.add(project)
    session.commit()
    print(f"✅ Project '{title}' added under client '{client_name}'.")

def list_projects():
    session = Session()
    projects = session.query(Project).all()
    for p in projects:
        print(f"[{p.id}] {p.title} - Client: {p.client.name}, Priority: {p.priority}, Deadline: {p.deadline}")

def add_task(project_title, description):
    session = Session()
    project = session.query(Project).filter_by(title=project_title).first()
    if not project:
        print(f"❌ Project '{project_title}' not found.")
        return
    session.add(Task(description=description, project=project))
    session.commit()
    print("✅ Task added.")

def mark_task_complete(task_id):
    session = Session()
    task = session.query(Task).get(task_id)
    if not task:
        print("❌ Task not found.")
        return
    task.complete = True
    session.commit()
    print("✅ Task marked complete.")

def task_progress_report():
    session = Session()
    projects = session.query(Project).all()
    for p in projects:
        total = len(p.tasks)
        done = len([t for t in p.tasks if t.complete])
        percent = (done / total) * 100 if total > 0 else 0
        print(f"{p.title}: {done}/{total} complete ({percent:.0f}%)")

def log_payment(project_title, amount, status, date=None):
    session = Session()
    project = session.query(Project).filter_by(title=project_title).first()
    if not project:
        print(f"❌ Project '{project_title}' not found.")
        return
    date = datetime.strptime(date, "%Y-%m-%d").date() if date else datetime.today().date()
    payment = Payment(amount=amount, status=status, date=date, project=project)
    session.add(payment)
    session.commit()
    print(f"✅ Payment logged for '{project_title}'.")

def view_payments():
    session = Session()
    payments = session.query(Payment).all()
    for p in payments:
        print(f"[{p.id}] {p.project.title} - {p.amount:.2f} on {p.date} ({p.status})")

def export_payments_csv(filename):
    session = Session()
    payments = session.query(Payment).all()
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Project", "Amount", "Date", "Status"])
        for p in payments:
            writer.writerow([p.id, p.project.title, f"{p.amount:.2f}", p.date, p.status])
    print(f"✅ Exported to {filename}")