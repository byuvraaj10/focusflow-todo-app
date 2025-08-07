# FocusFlow - To-Do List App with Streamlit

FocusFlow is a simple to-do list web app built using Streamlit. It allows you to add, view, complete, delete, and export tasks. Tasks are stored locally in a JSON file and include due dates, priorities, and status tracking.

## Features

- Add new tasks with description, due date, and priority
- View all tasks in a clean layout
- Mark tasks as complete or incomplete
- See a visual progress bar for completed tasks
- Filter tasks by keyword or status
- Sort tasks by due date, priority, status, or created time
- Export tasks to a CSV file
- Delete selected tasks

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/focusflow-todo-app.git
   cd focusflow-todo-app
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run todo.py
   ```

## Files

- `todo.py` – Main Streamlit application
- `tasks.json` – Local file used to store tasks (auto-generated)
- `requirements.txt` – Python dependencies
- `README.md` – Project overview


This project is open-source and available under the MIT License.
