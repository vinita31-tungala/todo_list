from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = "todo.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        tasks = conn.execute("SELECT * FROM todos WHERE status = 'pending'").fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form['text']  # ✅ changed from 'task' to 'text'
    if task_text.strip():
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO todos (text) VALUES (?)", (task_text,))
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("UPDATE todos SET status = 'completed' WHERE id = ?", (task_id,))
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("UPDATE todos SET status = 'deleted' WHERE id = ?", (task_id,))
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    new_text = request.form['edited_task']
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("UPDATE todos SET text = ? WHERE id = ?", (new_text, task_id))
    return redirect(url_for('index'))

@app.route('/completed')
def completed():
    with sqlite3.connect(DATABASE) as conn:
        tasks = conn.execute("SELECT * FROM todos WHERE status = 'completed'").fetchall()
    return render_template('index.html', tasks=tasks, show='completed')

@app.route('/deleted')
def deleted():
    with sqlite3.connect(DATABASE) as conn:
        tasks = conn.execute("SELECT * FROM todos WHERE status = 'deleted'").fetchall()
    return render_template('index.html', tasks=tasks, show='deleted')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)




