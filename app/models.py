from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    projects = relationship("Project", back_populates="client")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    priority = Column(String)
    deadline = Column(Date)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship("Client", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    payments = relationship("Payment", back_populates="project")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    complete = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(String)
    date = Column(Date)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="payments")