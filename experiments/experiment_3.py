import json
import sqlite3
from sqlite3 import Connection
import sqlite_vec 
from sqlite_vec import serialize_float32

json_question = './data/experiment_3/question_embeddings.json'
json_file = './data/experiment_3/epo_sample_embeddings_dataset.json'
db_name = '../epo.db'

#====
# Examine the json data file
#====
with open(json_file, 'r') as json_data:
    data = json.load(json_data)

# pprint(data)
print(type(data),
      data[0].keys(),
      )
database_len = len(data)

embed_len = 0
for key, value in data[0].items():
    print(f"type of {key}: {type(value)}")
    if (key == 'embeddings'):
        print(len(data[0][key]))

#====
# Functions
#====
def create_table(conn: Connection):

    sql_statement = """
    CREATE TABLE IF NOT EXISTS meta_data_embeddings (
            ipc TEXT,
            title TEXT NOT NULL, 
            claims TEXT NOT NULL, 
            claims_length INTEGER NOT NULL
        );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        conn.commit()
    except:
        print("Failed to create meta table")

def create_embed_table(conn: Connection, embedding_length: str):

    try:
        # load the extention
        conn.enable_load_extension(True) # start loading extensions
        sqlite_vec.load(conn)
        conn.enable_load_extension(True) # end loading extensions

        sql_statement = f"""
        CREATE VIRTUAL TABLE vec_items USING vec0(
            ipc TEXT partition key, 
            embedding float[{embedding_length}]);
        """
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        conn.commit()
    except:
        print("Failed to create embedding tables")

def add_to_meta_data(conn: Connection, table_data):
    # insert table statement
    sql = """ INSERT INTO meta_data_embeddings(rowid,title,claims,claims_length,ipc)
              VALUES(?,?,?,?,?) 
            """
    try:
        # Create  a cursor
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(sql, table_data)

        # commit the changes
        conn.commit()
    except:
        print("Failed to add datat to table.")

    # get the id of the last inserted row
    return cur.lastrowid

def add_embeddings(conn: Connection, table_data):
    # insert table statement
    sql = "INSERT INTO vec_items(rowid, embedding, ipc) VALUES (?, ?, ?)"
    try:
        conn.enable_load_extension(True) # start loading extensions
        sqlite_vec.load(conn)
        conn.enable_load_extension(True) # end loading extensions
        # Create  a cursor
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(sql, table_data)

        # commit the changes
        conn.commit()
    except:
        print("Failed to add datat to embedding table.")

    # get the id of the last inserted row
    return cur.lastrowid

def delete_embed_table(conn: Connection):
    try:
            conn.enable_load_extension(True) # start loading extensions
            sqlite_vec.load(conn)
            conn.enable_load_extension(True) # end loading extensions

            sql = 'DROP TABLE IF EXISTS vec_items;'
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to delete to embedding table.")

def delete_meta_table(conn: Connection):
    try:
            sql = 'DROP TABLE IF EXISTS meta_data_embeddings;'
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Failed to delete to meta table.")
#====
# Create meta table
#====
create_meta_table_state = False

if create_meta_table_state == True:
    try:
        with sqlite3.connect(db_name) as conn:
            create_table(conn)
            print("Tables created successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to connect to database", e)

#====
# Create embeddings table
#====
create_embed_table_state = False

if create_embed_table_state == True:
    try:
        with sqlite3.connect(db_name) as conn:
            create_embed_table(conn, str(len(data[0]['embeddings'])))
            print("Embeddings table created successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to connect to database", e)

#====
# Add to meta data of embedding table
#====
num_entries = database_len
add_data_state = False
if add_data_state == True:
    try:
        with sqlite3.connect(db_name) as conn:
        
            for i in range(0, num_entries):
                add_to_meta_data(conn, (int(i),
                                        data[i]['title'], 
                                        data[i]['claims'], 
                                        data[i]['claims_length'],
                                        data[i]['ipc']
                                        )
                                )
            print("Successfully add data to meta table")
    except sqlite3.OperationalError as e:
        print("Failed to connect to db")

#====
# Add to embeddings data 
#====
add_embed_state = False
if add_embed_state == True:
    try:
        with sqlite3.connect(db_name) as conn:
            for i in range(0, num_entries):
                add_embeddings(conn,[i, serialize_float32(data[i]['embeddings']), data[i]['ipc']])
            print("Successfully add data to embed table")
    except sqlite3.OperationalError as e:
        print("Failed to connect to db")

#====
# Delete all tables in sqlite db
# ref: https://stackoverflow.com/questions/525512/drop-all-tables-command
# FAIL: `sqlite_master may not be modified`
#====
del_all_table_state = False
if del_all_table_state == True:
    try:
        with sqlite3.connect(db_name) as conn:
            conn.enable_load_extension(True) # start loading extensions
            sqlite_vec.load(conn)
            conn.enable_load_extension(True) # end loading extensions
            sql = """delete from sqlite_master where type in ('table', 'index', 'trigger');"""
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            print("Successfully del all tables")
    except sqlite3.OperationalError as e:
        print("Fail reason:", e)

# 
#====
# Delete embeddings table
#====
del_embed_table_state = False
if del_embed_table_state == True:
    try:
        with sqlite3.connect(db_name) as conn:
            delete_embed_table(conn)
            print("Successfully del embed table")
    except sqlite3.OperationalError as e:
        print("Failed to connect to db")

#====
# Delete meta table
#====
del_meta_table_state = False
if del_meta_table_state == True:
    try:
        with sqlite3.connect(db_name) as conn:
            delete_meta_table(conn)
            print("Successfully del meta table")
    except sqlite3.OperationalError as e:
        print("Failed to connect to db")

#====
# check
#====
try:
    with sqlite3.connect(db_name) as conn:

        conn.enable_load_extension(True) # start loading extensions
        sqlite_vec.load(conn)
        conn.enable_load_extension(True) # end loading extensions

        # Check the loading extension successfully?
        sqlite_version, vec_version = conn.execute(
        "select sqlite_version(), vec_version()"
        ).fetchone()
        print(f"sqlite_version={sqlite_version}, vec_version={vec_version}")

        # Check the state of tables in db
        cur = conn.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        print(res.fetchall())

        # # Check all available tables in the databse
        # cursor = conn.cursor()
        # res = cursor.execute("SELECT name FROM sqlite_master")
        # print(f"{'='*10}")
        # print(res.fetchall())

        # # Check data in the embedding table
        # cursor = conn.cursor()
        # res = cursor.execute("SELECT * FROM vec_items_rowids")
        # print(f"{'='*10}")
        # print(res.fetchall())

        # # Check data in the mata table
        # meta_query = """
        # SELECT
        #     rowid
        # FROM meta_data_embeddings
        # """
        # cursor = conn.cursor()
        # res = cursor.execute(meta_query)
        # print(f"{'='*10}")
        # print(res.fetchall())

        # meta_query = """
        # SELECT
        #     title
        # FROM meta_data_embeddings
        # WHERE rowid=1
        # """
        # cursor = conn.cursor()
        # res = cursor.execute(meta_query)
        # print(f"{'='*10}")
        # print(res.fetchall())

except sqlite3.OperationalError as e:
    print(e)
