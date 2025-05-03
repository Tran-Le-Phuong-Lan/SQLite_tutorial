import sqlite3 
import sqlite_vec 

try:
    with sqlite3.connect('../my.db') as conn:

        # load the `sqlite-vec` extention into the connected db
        ## NOTE:
        # must load the `sqlite-vec` extention everytime connect to the db, 
        # in order to use the vec table created using extension `sqlte-vec` and `sqlite-vec` functions
        conn.enable_load_extension(True) # start loading extensions
        sqlite_vec.load(conn)
        conn.enable_load_extension(True) # end loading extensions

        sql = 'DROP TABLE IF EXISTS vec_items;'
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        sql = 'SELECT * FROM sqlite_sequence;'
        res = cursor.execute(sql)
        print(f"{'='*10}")
        print(res.fetchall())

        # Check all available tables in the databse
        cursor = conn.cursor()
        res = cursor.execute("SELECT name FROM sqlite_master")
        print(f"{'='*10}")
        print(res.fetchall())

except sqlite3.OperationalError as e:
    print(e)