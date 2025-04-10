from calendar import c
from flask import Flask, request, render_template, redirect
import sqlite3


print("App is starting...")


app = Flask(__name__)

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect('database.db')
    
    c = conn.cursor()
        # Insert a default user for testing
 


    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
    # Add a test user
   
    conn.commit()
    conn.close()

# ---------- ROUTES ----------
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🚨 Vulnerable to SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"[DEBUG] Executing SQL: {query}")  # For demo

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute(query)
            user = c.fetchone()
            if user:
                message = "Login successful! 🎉"
            else:
                message = "Invalid credentials."
        except Exception as e:
            message = f"Error: {str(e)}"
        conn.close()

    return render_template('login.html', message=message)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
