from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///freelance_tracker.db')
Session = sessionmaker(bind=engine)
