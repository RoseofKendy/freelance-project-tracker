from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
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
    is_recurring = Column(Boolean, default=False)
    recurrence_interval = Column(String)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    complete = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")
    time_logs = relationship("TimeLog", back_populates="task", cascade="all, delete")
    is_recurring = Column(Boolean, default=False)
    recurrence_interval = Column(String)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(String)
    date = Column(Date)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="payments")

class TimeLog(Base):
    __tablename__ = 'time_logs'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    task = relationship("Task", back_populates="time_logs")

    def duration_minutes(self):
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds() / 60)
        return None