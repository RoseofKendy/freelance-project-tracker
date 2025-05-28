from app.database import Session
from app.models import Client

def add_client(name):
    session = Session()
    client = Client(name=name)
    session.add(client)
    session.commit()
    print(f"Client '{name}' added.")

def list_clients():
    session = Session()
    clients = session.query(Client).all()
    for client in clients:
        print(client.name)
