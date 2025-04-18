import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

print("Users Table:")
for row in c.execute('SELECT * FROM users'):
    print(row)

print("\nProducts Table:")
for row in c.execute('SELECT * FROM products'):
    print(row)

conn.close()
