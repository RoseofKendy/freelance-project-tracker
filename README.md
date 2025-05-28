# Freelance Project Tracker

A command-line interface (CLI) tool for freelancers to manage their clients, projects, tasks, and payments efficiently.

---

## 🚀 Features

- **Client & Project Management**: Create and organize projects by client, priority, and deadline.
- **Task Tracking**: Add tasks, mark as complete, and monitor progress percentage.
- **Payment Logging**: Record invoices, received payments, and pending dues.
- **Database Integration**: Structured storage using SQLite and SQLAlchemy.

---

## 🛠 Tech Stack

- Python 3.x
- SQLAlchemy
- Click (CLI tool)
- SQLite (Local Database)
- Tabulate (for formatted CLI tables)

---

## ⚙️ Setup Instructions

1. **Clone the repo:**
   ```bash
   git clone https://github.com/your-username/freelance_project_tracker.git
   cd freelance_project_tracker

Create & activate virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Initialize the database:

bash
Copy code
python main.py
Run CLI commands:

bash
Copy code
python main.py addclient "Acme Inc."
📝 TODO
 Add export to CSV functionality

 Add deadline notifications

 Add dashboard summaries

