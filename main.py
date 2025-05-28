from app.database import Base, engine
from app.cli import cli  # will define later

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    cli()
