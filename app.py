from flask import Flask, render_template, request, redirect, url_for
import sqlite3, datetime
from utils.scheduler import start_scheduler

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT, description TEXT,
                  due_date TEXT, category TEXT,
                  priority TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY due_date")
    tasks = c.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=["GET","POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        category = request.form["category"]
        priority = request.form["priority"]

        conn = sqlite3.connect("tasks.db")
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title, description, due_date, category, priority, status) VALUES (?,?,?,?,?,?)",
                  (title, description, due_date, category, priority, "Pending"))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("add_task.html")

@app.route('/complete/<int:task_id>', methods=["POST"])
def complete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", ("Completed", task_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    start_scheduler()   # Start background reminder checker
    app.run(debug=True)
