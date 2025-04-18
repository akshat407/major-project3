from flask import Flask, request, render_template_string, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret'

DB_PATH = 'shop.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)''')
    c.execute("INSERT INTO products (name, price) VALUES ('Sneakers', 49.99), ('T-Shirt', 19.99), ('Jeans', 39.99)")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template_string('''
        <h1>Product List</h1>
        <ul>
            {% for p in products %}
                <li><a href="/product/{{p[0]}}">{{p[1]}}</a> - ${{p[2]}}</li>
            {% endfor %}
        </ul>
        <a href="/login">Login</a> | <a href="/register">Register</a>
    ''', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw))
        if c.fetchone():
            session['user'] = user
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return '''<form method="post">Username: <input name="username"> Password: <input name="password" type="password"><input type="submit"></form>'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pw))
        conn.commit()
        return redirect(url_for('login'))
    return '''<form method="post">Username: <input name="username"> Password: <input name="password" type="password"><input type="submit"></form>'''

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f"<h1>Search Results for: {query}</h1>"  # Vulnerable to reflected XSS

@app.route('/product/<id>')
def product(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Vulnerable to SQLi
        c.execute(f"SELECT * FROM products WHERE id = {id}")
        product = c.fetchone()
    except:
        product = None
    conn.close()
    if product:
        return f"<h1>{product[1]}</h1><p>Price: ${product[2]}</p>"
    return "Product not found"

@app.route('/admin', methods=['GET'])
def admin():
    cmd = request.args.get('cmd', '')
    try:
        output = os.popen(cmd).read()  # Vulnerable to command injection
    except:
        output = 'Error executing command'
    return f"<h1>Admin Panel</h1><pre>{output}</pre>"

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)
