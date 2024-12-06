from flask import Flask, jsonify, request, render_template_string, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  completed BOOLEAN NOT NULL DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Enhanced Todo List</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .completed { text-decoration: line-through; color: #888; }
        .task-item { display: flex; align-items: center; margin: 8px 0; }
        .timestamp { font-size: 0.8em; color: #666; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="mb-4">Todo List</h1>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-info">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form action="/add" method="POST" class="mb-4">
            <div class="input-group">
                <input type="text" name="task" class="form-control" placeholder="Enter a new task" required>
                <button type="submit" class="btn btn-primary">Add Task</button>
            </div>
        </form>

        <div class="list-group">
            {% for task in tasks %}
            <div class="list-group-item task-item">
                <input type="checkbox" onchange="window.location.href='/toggle/{{task[0]}}'"
                       {% if task[2] %}checked{% endif %}>
                <span class="ms-2 {% if task[2] %}completed{% endif %}">{{ task[1] }}</span>
                <small class="timestamp ms-2">{{ task[3] }}</small>
                <a href="/delete/{{task[0]}}" class="btn btn-danger btn-sm ms-auto">Delete</a>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    tasks = c.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('INSERT INTO tasks (title) VALUES (?)', (task,))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = NOT completed WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
