import sqlite3

sql = 'DELETE FROM tasks WHERE id = ?'

try:
    with sqlite3.connect('my.db') as conn:
        cur = conn.cursor()
        cur.execute(sql, (1,))
        conn.commit()
except sqlite3.OperationalError as e:
    print(e)