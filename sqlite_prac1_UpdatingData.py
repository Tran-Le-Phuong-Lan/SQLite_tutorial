import sqlite3

# # 1. Updating one field of one row in a table
# ## For example, select the row whose `id`` = 2, and update its field `priority` to 2
# sql = 'UPDATE tasks SET priority = ? WHERE id = ?'
# try:
#     with sqlite3.connect('my.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql, (2,1) )
#         conn.commit()
# except sqlite3.OperationalError as e:
#     print(e)

# # 2. Updating multiple columns (i.e fields) of one row in a table
# ## For example, select the row whose `id`` = 2, and update its field `priority` to 3, update its field `status_id` to 2
# sql = 'UPDATE tasks SET priority = ?, status_id = ? WHERE id = ?'

# try:
#     with sqlite3.connect('my.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql, (3,2,1) )
#         conn.commit()
# except sqlite3.OperationalError as e:
#     print(e)

# # 3. Updating multiple columns of multiple rows in a table
# ## Example: The following program illustrates how to update the `end_date` columns of all the tasks to `2015-02-03`
# sql = 'UPDATE tasks SET end_date = ?'

# try:
#     with sqlite3.connect('my.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute(sql, ('2015-02-03',) )
#         conn.commit()
# except sqlite3.Error as e:
#     print(e)