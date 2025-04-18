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

from flask import request

@app.before_request
def extract_request_data():
    method = request.method  # GET, POST, etc.
    user_agent = request.headers.get('User-Agent', 'Unknown')
    url = request.url  # Full URL
    content = request.get_data(as_text=True)  # Request body (for POST/PUT)
    cookie = request.cookies  # Dictionary of cookies
    
    if request.content_type == 'application/json':
        request_json = request.json  # Parsed JSON data
        print(f"Request JSON: {request_json}")
    else:
        print("Request JSON: Unsupported Media Type")
    print(f"Method: {method}")
    print(f"User-Agent: {user_agent}")
    print(f"URL: {url}")
    print(f"Content: {content}")
    print(f"Cookie: {cookie}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    response_data = {}
    if request.method == 'POST':
        # Extract request data
        method = request.method
        user_agent = request.headers.get('User-Agent', 'Unknown')
        url = request.url
        content = request.get_data(as_text=True)
        cookie = request.cookies


        # Log extracted data
        print(f"Method: {method}")
        print(f"User-Agent: {user_agent}")
        print(f"URL: {url}")
        print(f"Content: {content}")
        print(f"Cookie: {cookie}")

        # Add extracted data to response
        response_data['method'] = method
        response_data['user_agent'] = user_agent
        response_data['url'] = url
        response_data['content'] = content
        response_data['cookie'] = cookie

        # Handle login logic
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            c.execute(query, (username, password))
            user = c.fetchone()
            if user:
                response_data['message'] = "Login successful! 🎉"
            else:
                response_data['message'] = "Invalid credentials."
        except Exception as e:
            response_data['message'] = f"Error: {str(e)}"
        finally:
            conn.close()

        # Return JSON response
        return response_data

    # For GET requests, return a default message
    return {"message": "Please use POST to login."}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
