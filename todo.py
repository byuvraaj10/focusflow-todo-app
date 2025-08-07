import streamlit as st
import json
import os
from datetime import datetime, date
import pandas as pd

# ---- Constants ----
TASKS_FILE = "tasks.json"

# ---- Utility Functions ----
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def toggle_done(index):
    st.session_state.tasks[index]["done"] = not st.session_state.tasks[index]["done"]
    save_tasks(st.session_state.tasks)

def calculate_progress():
    total = len(st.session_state.tasks)
    done = sum(1 for task in st.session_state.tasks if task["done"])
    return (done / total * 100) if total > 0 else 0

def export_tasks():
    df = pd.DataFrame(st.session_state.tasks)
    df.to_csv("exported_tasks.csv", index=False)
    return "exported_tasks.csv"

# ---- Initialize Tasks ----
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ---- Page Config ----
st.set_page_config(page_title="FocusFlow", layout="wide")
st.markdown("<h1 style='text-align: center; color:#4CAF50;'>🧠 FocusFlow</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color:#888;'>Organize your day. Prioritize what matters. Complete with confidence.</h3>", unsafe_allow_html=True)

# ---- Description ----
with st.expander("ℹ️ What is FocusFlow?"):
    st.write("""
    **FocusFlow** is your personal task companion built using **Streamlit**.  
    Add, prioritize, and manage your tasks with ease using intuitive UI elements.  
    Features include due dates, priorities, progress tracking, task filters, and export capability.
    """)

# ---- Sidebar: Add Task ----
st.sidebar.header("➕ Add New Task")
with st.sidebar.form("task_form"):
    task_desc = st.text_input("🖊️ Task Description")
    due_date = st.date_input("📅 Due Date")
    priority = st.selectbox("⭐ Priority", ["Low", "Medium", "High"])
    add = st.form_submit_button("Add Task")
    if add:
        if task_desc.strip():
            st.session_state.tasks.append({
                "task": task_desc,
                "done": False,
                "due": str(due_date),
                "priority": priority,
                "created_at": str(datetime.now())
            })
            save_tasks(st.session_state.tasks)
            st.success("✅ Task added!")
        else:
            st.warning("❗ Please enter a task description.")

# ---- Sidebar: Filter & Export ----
st.sidebar.header("🔍 Filter Tasks")
search = st.sidebar.text_input("Search by keyword")
show_pending = st.sidebar.checkbox("Show only pending tasks")
sort_by = st.sidebar.selectbox("Sort by", ["Created Time", "Due Date", "Priority", "Status"])

if st.sidebar.button("📤 Export Tasks as CSV"):
    file_path = export_tasks()
    st.sidebar.success(f"Exported to {file_path}")

# ---- Filter and Sort Tasks ----
def sort_key(task):
    if sort_by == "Created Time":
        return task.get("created_at", "")
    elif sort_by == "Due Date":
        return task.get("due", "")
    elif sort_by == "Priority":
        return {"High": 1, "Medium": 2, "Low": 3}.get(task.get("priority", "Low"), 3)
    elif sort_by == "Status":
        return task["done"]
    return task["task"]

filtered_tasks = [
    (i, task) for i, task in enumerate(st.session_state.tasks)
    if search.lower() in task["task"].lower()
    and (not show_pending or not task["done"])
]
filtered_tasks.sort(key=lambda x: sort_key(x[1]))

# ---- Progress Bar ----
st.subheader("📊 Task Progress")
progress = calculate_progress()
st.progress(progress / 100)
st.write(f"✅ {int(progress)}% completed")

# ---- Task Display ----
st.subheader("📋 Your Tasks")
if filtered_tasks:
    for i, task in filtered_tasks:
        col1, col2, col3, col4, col5 = st.columns([0.05, 0.4, 0.2, 0.15, 0.2])

        col1.checkbox(
            "", 
            value=task["done"], 
            key=f"done_{i}", 
            on_change=toggle_done, 
            args=(i,)
        )

        due_status = ""
        if not task["done"] and task["due"] < str(date.today()):
            due_status = "🔥 Overdue!"
        elif not task["done"]:
            due_status = "⌛ Upcoming"
        else:
            due_status = "✅ Done"

        priority_color = {
            "High": "red",
            "Medium": "orange",
            "Low": "green"
        }.get(task["priority"], "gray")

        col2.markdown(f"**{task['task']}**")
        col3.markdown(f"📅 {task['due']}  \n<span style='color:red;'>{due_status}</span>", unsafe_allow_html=True)
        col4.markdown(f"<span style='color:{priority_color}; font-weight:bold;'>⭐ {task['priority']}</span>", unsafe_allow_html=True)
        col5.markdown("🕓 " + task["created_at"].split(" ")[0])
else:
    st.info("No tasks found.")

# ---- Delete Task ----
st.subheader("🗑️ Delete Task")
if st.session_state.tasks:
    task_names = [f"{i+1}. {task['task']}" for i, task in enumerate(st.session_state.tasks)]
    selected = st.selectbox("Select task to delete", task_names)
    if st.button("Delete Task"):
        index = int(selected.split(".")[0]) - 1
        removed = st.session_state.tasks.pop(index)
        save_tasks(st.session_state.tasks)
        st.success(f"🗑️ Deleted task: {removed['task']}")
else:
    st.info("No tasks to delete.")
