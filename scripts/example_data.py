from app.database import Base, engine, Session
from app.models import Client, Project, Task, Payment, TimeLog
from datetime import date

Base.metadata.create_all(engine)
session = Session()

client = Client(name="Clarion Hotel")
project = Project(title="Website Redesign", priority="High", deadline=date(2025, 7, 30), client=client)
tasks = [
    Task(description="Design mockups", complete=True, project=project),
    Task(description="Implement frontend", complete=False, project=project)
]
payments = [
    Payment(amount=300.00, status="received", date=date(2025, 6, 10), project=project),
    Payment(amount=200.00, status="pending", date=date(2025, 7, 1), project=project)
]

session.add(client)
session.add_all(tasks + payments)
session.commit()
print("✅ Example data added.")
