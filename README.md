# 💼 Freelance Project Tracker

A simple, lightweight **command-line tool** to help freelancers manage clients, projects, tasks, and payments — all in one place.

---

## 🚩 Problem Statement

Freelancers often juggle multiple clients and projects without a centralized way to track:
- Project progress
- Task completion
- Payment status

---

## ✅ Solution

The Freelance Project Tracker offers a **CLI-based system** that allows you to:
- Add clients and projects
- Track task completion and progress
- Log received and pending payments
- Store everything in a structured database

---

## 🧰 Features (MVP)

| Feature               | Description                                                      |
|-----------------------|------------------------------------------------------------------|
| Client Management     | Add and list clients                                             |
| Project Management    | Organize projects by client, priority, and deadline             |
| Task Tracking         | Add tasks, mark as complete, and view progress reports          |
| Payment Logging       | Record received or pending payments with dates                  |
| Database Integration  | SQLAlchemy + SQLite backend for persistent storage              |

---

## 📦 Tech Stack

- Python 3.10+
- Click (for CLI)
- SQLAlchemy (ORM)
- SQLite (lightweight database)
- WSL Ubuntu 22.04 or any Linux/macOS environment

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/freelance-project-tracker.git
cd freelance-project-tracker
2. Set up virtual environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
🚀 Usage
Run the main CLI:

bash
Copy code
python main.py [COMMAND]
🎯 Client Commands
bash
Copy code
python main.py addclient "Client Name"
python main.py listclients
📋 Project Commands
bash
Copy code
python main.py addproject "Project Title" "Client Name" --priority High --deadline 2025-07-01
python main.py listprojects
✅ Task Commands
bash
Copy code
python main.py addtask "Project Title" "Design homepage layout"
python main.py marktaskcomplete 1
python main.py progressreport
💵 Payment Commands
bash
Copy code
python main.py logpayment "Project Title" 500.00 received --date 2025-06-01
python main.py viewpayments
🧪 Example Walkthrough
bash
Copy code
# Add a new client
python main.py addclient "Clarion Inc"

# Create a project
python main.py addproject "Website Revamp" "Clarion Inc" --priority High --deadline 2025-07-01

# Add tasks
python main.py addtask "Website Revamp" "Design homepage"
python main.py addtask "Website Revamp" "Implement backend"

# Mark a task complete
python main.py marktaskcomplete 1

# Log a payment
python main.py logpayment "Website Revamp" 1000 received --date 2025-06-15

# View reports
python main.py progressreport
python main.py viewpayments
📁 Project Structure
bash
Copy code
freelance_project_tracker/
│
├── app/
│   ├── cli.py          # Click CLI commands
│   ├── database.py     # DB setup
│   ├── models.py       # SQLAlchemy models
│   └── utils.py        # Feature logic
│
├── main.py             # Entry point
├── requirements.txt    # Dependencies
├── .gitignore
└── README.md
💡 Future Enhancements
Export reports to CSV

Add authentication for multi-user usage

Generate invoice templates

Search and filter functionality

Package as a Python pip installable CLI tool

👩🏽‍💻 Author
Njue Sharon Kendi
Freelancer & Software Developer
Moringa School