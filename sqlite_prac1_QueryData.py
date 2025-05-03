import sqlite3

# Querying all rows from a table example
print(f"{'='*10}")
print(f"Querying all rows from a table example")
try:
    with sqlite3.connect('my.db') as conn:
        cur = conn.cursor()
        cur.execute('select id, name, priority from tasks')
        rows = cur.fetchall()
        for row in rows:
            print(row)
except sqlite3.OperationalError as e:
    print(e)

# Querying data with parameters
print(f"{'='*10}")
print(f"Querying data with parameters")
try:
    with sqlite3.connect('my.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, name, priority FROM tasks WHERE id =?', (1,))
        row = cur.fetchone()
        if row:
            print(row)
except sqlite3.OperationalError as e:
    print(e)
