import json
import sqlite3
from sqlite3 import Connection
import sqlite_vec
from sqlite_vec import serialize_float32

# import the question embedding
json_question = './data/experiment_3/question_embeddings.json'
db_name = '../epo.db'

#====
# Examine the json data file
#====
with open(json_question, 'r') as json_data:
    q_data = json.load(json_data)

print(
    type(q_data),
    q_data.keys(),
    type(q_data['question']),
    len(q_data['question'][0]),
    type(q_data['question'][0]))

try:
    with sqlite3.connect(db_name) as conn:

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

        # Query to the created vec table
        query = q_data['question'][0]
        rows = conn.execute(
        """
        SELECT
            rowid,
            distance
        FROM vec_items
        WHERE embedding MATCH ?
        ORDER BY distance
        LIMIT 1
        """,
        [serialize_float32(query)],
        ).fetchall()

        print(f"{'='*10}")
        print(rows)

         # Check data in the mata table
        meta_query = f"""
        SELECT
            claims
        FROM meta_data_embeddings
        WHERE rowid={int(rows[0][0] + 1)}
        """
        cursor = conn.cursor()
        res = cursor.execute(meta_query)
        print(f"{'='*10}")
        print(res.fetchall())

except sqlite3.OperationalError as e:
    print(e)