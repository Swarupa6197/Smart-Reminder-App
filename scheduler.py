from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3, datetime
from utils.email_sender import send_email

def check_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT id, title, due_date, status FROM tasks")
    tasks = c.fetchall()
    now = datetime.datetime.now()

    for task in tasks:
        task_id, title, due_date, status = task
        due = datetime.datetime.strptime(due_date, "%Y-%m-%d %H:%M")

        # If overdue
        if due < now and status == "Pending":
            c.execute("UPDATE tasks SET status=? WHERE id=?", ("Overdue", task_id))
            send_email("yourmail@gmail.com", f"Task '{title}' is overdue!", "Please check your dashboard.")
        
        # If due in 1 hour
        elif (due - now).total_seconds() < 3600 and status == "Pending":
            send_email("yourmail@gmail.com", f"Reminder: Task '{title}'", "Your task is due within 1 hour!")

    conn.commit()
    conn.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_tasks, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started, checking tasks every minute.")