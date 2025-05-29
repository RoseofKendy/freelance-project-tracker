# models.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Base class for our declarative models
Base = declarative_base()

class Client(Base):
    """
    Represents a client in the freelance project tracker.
    Each client can have multiple projects.
    """
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)

    # One-to-many relationship with Project
    projects = relationship("Project", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}')>"

class Project(Base):
    """
    Represents a project associated with a client.
    Projects have tasks and can have payments.
    """
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    deadline = Column(DateTime)
    priority = Column(String, default='Medium') # e.g., High, Medium, Low
    status = Column(String, default='Pending') # e.g., Pending, In Progress, Completed, On Hold

    # Foreign key to Client
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship("Client", back_populates="projects")

    # One-to-many relationship with Task and Payment
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', client='{self.client.name if self.client else 'N/A'}')>"

    def get_progress_percentage(self):
        """Calculates the completion percentage of tasks for this project."""
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return 0
        completed_tasks = sum(1 for task in self.tasks if task.is_completed)
        return (completed_tasks / total_tasks) * 100

class Task(Base):
    """
    Represents a task within a project.
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)

    # Foreign key to Project
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, description='{self.description[:30]}...', completed={self.is_completed})>"

class Payment(Base):
    """
    Represents a payment record for a project.
    Can be a logged invoice, received payment, or pending amount.
    """
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    payment_type = Column(String, nullable=False) # e.g., 'Invoice', 'Received', 'Pending'
    date = Column(DateTime, default=datetime.now)
    notes = Column(Text)

    # Foreign key to Project
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, type='{self.payment_type}')>"
