from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"
DATABASE = "todo.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                deadline TEXT,
                position INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    filter_status = request.args.get('filter', 'pending')
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row  # ✅ Convert tuples to dict-like rows
        cursor = conn.cursor()
        if filter_status == 'all':
            tasks = cursor.execute(
                "SELECT * FROM todos WHERE user_id = ? ORDER BY position",
                (session['user_id'],)
            ).fetchall()
        else:
            tasks = cursor.execute(
                "SELECT * FROM todos WHERE user_id = ? AND status = ? ORDER BY position",
                (session['user_id'], filter_status)
            ).fetchall()
    return render_template('index.html', tasks=tasks, current_filter=filter_status)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    task_text = request.form['text']
    deadline = request.form.get('deadline')
    
    if task_text.strip():
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                """
                INSERT INTO todos (user_id, text, deadline, position)
                VALUES (?, ?, ?, (SELECT IFNULL(MAX(position), 0) + 1 FROM todos WHERE user_id = ?))
                """,
                (session['user_id'], task_text, deadline, session['user_id'])
            )
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "UPDATE todos SET status = 'completed' WHERE id = ? AND user_id = ?",
            (task_id, session['user_id'])
        )
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "UPDATE todos SET status = 'deleted' WHERE id = ? AND user_id = ?",
            (task_id, session['user_id'])
        )
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_text = request.form['edited_task']
    deadline = request.form.get('deadline')
    
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "UPDATE todos SET text = ?, deadline = ? WHERE id = ? AND user_id = ?",
            (new_text, deadline, task_id, session['user_id'])
        )
    return redirect(url_for('index'))

@app.route('/update_positions', methods=['POST'])
def update_positions():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    positions = request.get_json()
    with sqlite3.connect(DATABASE) as conn:
        for index, task_id in enumerate(positions['order']):
            conn.execute(
                "UPDATE todos SET position = ? WHERE id = ? AND user_id = ?",
                (index, task_id, session['user_id'])
            )
    return jsonify({'status': 'success'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect(DATABASE) as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            ).fetchone()
        
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        return "Invalid credentials"
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect(DATABASE) as conn:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already taken"
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)







