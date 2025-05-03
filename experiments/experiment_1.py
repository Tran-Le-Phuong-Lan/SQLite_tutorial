import sqlite3 
import sqlite_vec 

from typing import List
import struct

create_vec_table = False

def serialize_f32(vector: List[float]) -> bytes:
    """serializes a list of floats into a compact "raw bytes" format"""
    return struct.pack("%sf" % len(vector), *vector)

try:
    with sqlite3.connect('../my.db') as conn:

        # load the `sqlite-vec` extention into the connected db
        ## NOTE:
        # must load the `sqlite-vec` extention everytime connect to the db, 
        # in order to use the vec table created using extension `sqlte-vec` and `sqlite-vec` functions
        conn.enable_load_extension(True) # start loading extensions
        sqlite_vec.load(conn)
        conn.enable_load_extension(True) # end loading extensions

        # Check the loading extension successfully?
        sqlite_version, vec_version = conn.execute(
        "select sqlite_version(), vec_version()"
        ).fetchone()
        print(f"sqlite_version={sqlite_version}, vec_version={vec_version}")

        # Create a virtual table of `sqlite-vec`
        if (create_vec_table == True):
            items = [
                (1, [0.1, 0.1, 0.1, 0.1]),
                (2, [0.2, 0.2, 0.2, 0.2]),
                (3, [0.3, 0.3, 0.3, 0.3]),
                (4, [0.4, 0.4, 0.4, 0.4]),
                (5, [0.5, 0.5, 0.5, 0.5]),
            ]

            conn.execute("CREATE VIRTUAL TABLE vec_items USING vec0(embedding float[4])")

            for item in items:
                conn.execute(
                    "INSERT INTO vec_items(rowid, embedding) VALUES (?, ?)",
                    [item[0], serialize_f32(item[1])]
                )

            conn.commit()
        
        # Query to the created vec table
        query = [0.3, 0.3, 0.3, 0.3]
        rows = conn.execute(
        """
        SELECT
            rowid,
            distance
        FROM vec_items
        WHERE embedding MATCH ?
        ORDER BY distance
        LIMIT 3
        """,
        [serialize_f32(query)],
        ).fetchall()

        print(f"{'='*10}")
        print(rows)
        
        # Check all available tables in the databse
        cursor = conn.cursor()
        res = cursor.execute("SELECT name FROM sqlite_master")
        print(f"{'='*10}")
        print(res.fetchall())

except sqlite3.OperationalError as e:
    print(e)