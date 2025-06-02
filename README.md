# Freelance Project Tracker CLI

## 📝 Description

The Freelance Project Tracker is a command-line interface (CLI) application designed to help freelancers manage their clients, projects, tasks, and payments efficiently. Built with Python, SQLAlchemy, and Click, it provides a simple yet powerful way to track project progress, log payments, and generate comprehensive reports directly from your terminal.

## ✨ Features

This CLI application offers a robust set of features to streamline your freelance workflow:

* **Client Management:**
    * `add-client`: Add new client details (name, contact person, email, phone).
    * `list-clients`: View a list of all your registered clients.
* **Project Management:**
    * `add-project`: Create new projects, linking them to existing clients, with options for description, deadline, and priority.
    * `list-projects`: List all projects, with an option to filter by client. Includes project status and progress percentage.
* **Task Tracking:**
    * `add-task`: Add individual tasks to specific projects.
    * `mark-task-complete`: Mark tasks as completed.
        * **Automatic Project Completion**: If all tasks within a project are marked complete, the project's status will automatically update to 'Completed'.
    * `progress-report`: View the task completion progress for projects.
* **Payment Logging:**
    * `log-payment`: Record payments received or invoiced for projects, including amount, type, and notes.
    * `view-payments`: See a list of all payments, with options to filter by project.
* **Advanced Reporting & Utilities:**
    * `export-to-csv`: Export all client, project, task, and payment data into a single CSV file for easy analysis or backup.
    * `search`: Search for specific terms across client, project, task, and payment details.
    * `comprehensive-report`: Generate a detailed report showing all clients, their projects, and associated tasks and payments, organized for clear readability.

## 🚀 Technologies Used

* **Python 3.x**: The core programming language.
* **Click**: A Python package for creating beautiful command-line interfaces.
* **SQLAlchemy ORM**: A powerful SQL toolkit and Object-Relational Mapper for interacting with the database.
* **SQLite**: A lightweight, file-based relational database used for data storage.
* **Alembic**: A database migration tool for SQLAlchemy, used for managing schema changes.
* **Pipenv**: A Python dependency management tool that combines pip and virtualenv functionalities.
* **Tabulate**: A library for printing data in neat, plain-text tables.

## ⚙️ Setup Instructions

Follow these steps to get your Freelance Project Tracker up and running:

### Prerequisites

* Python 3.x installed on your system.
* `pip` (Python's package installer), which usually comes with Python.

### 1. Install Pipenv (Globally)

If you don't have `pipenv` installed, run this command once globally:

```bash
pip install --user pipenv

2. Clone the Repository & Navigate
(Assuming you've downloaded or cloned the project files into a directory named freelance_tracker_pipenv)

Bash

# Navigate to where you want to keep your project
cd path/to/your/desired/directory

# Create the project folder (if you haven't already)
mkdir freelance_tracker_pipenv
cd freelance_tracker_pipenv
3. Set Up Virtual Environment & Install Dependencies
From within your freelance_tracker_pipenv directory, run:

Bash

pipenv install SQLAlchemy click tabulate alembic
This command will:

Create a virtual environment for your project if one doesn't exist.
Install all specified dependencies into that environment.
Create Pipfile and Pipfile.lock files to manage your project's dependencies.
4. Activate the Pipenv Shell
To work within your project's isolated environment:

Bash

pipenv shell
Your terminal prompt will change (e.g., (freelance_tracker_pipenv)) to indicate that the virtual environment is active. All subsequent commands for the project should be run from this activated shell.

5. Create Project Files
Ensure you have the following Python files in your freelance_tracker_pipenv directory. If you've been following the guide, you should already have them:

models.py
database.py
cli.py
6. Initialize and Configure Alembic
This sets up your database migration environment.

Initialize Alembic:

Bash

alembic init alembic
This creates an alembic folder and alembic.ini file.

Configure alembic.ini:
Open the alembic.ini file and change the sqlalchemy.url line to point to your SQLite database:

Ini, TOML

# alembic.ini
# ...
sqlalchemy.url = sqlite:///freelance_tracker.db
# ...
Configure alembic/env.py:
Open alembic/env.py (inside the alembic subfolder) and make these crucial changes to link Alembic to your models.py:

Python

# alembic/env.py
# ... (existing imports)
import os
import sys
from pathlib import Path

# Add your project's root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from models import Base # <--- ADD THIS LINE to import your Base

# ...
# Inside run_migrations_online() or run_migrations_offline()
# Find this line:
# target_metadata = None
# CHANGE IT TO:
target_metadata = Base.metadata # <--- CHANGE THIS LINE (uncomment if it's commented out)
# ...
7. Create and Apply Initial Database Migrations
Generate the first migration script: This will detect your models.py and create the SQL to build your tables.

Bash

alembic revision --autogenerate -m "Create initial tables"
A new Python file will be created in alembic/versions/.

Apply the migration to your database:

Bash

alembic upgrade head
This command will create your freelance_tracker.db file with all the necessary tables.

8. Run the Application
You are now ready to use the CLI!

Bash

# To see all available commands
python cli.py --help

# To see help for a specific command
python cli.py add-client --help

# To run a command (examples)
python cli.py add-client
python cli.py add-project
python cli.py add-task
python cli.py mark-task-complete
python cli.py log-payment
python cli.py view-payments
python cli.py list-projects
python cli.py list-clients
python cli.py comprehensive-report