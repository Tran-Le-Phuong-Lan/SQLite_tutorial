import sqlite3

def add_project(conn, project):
    # insert table statement
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    
    # Create  a cursor
    cur = conn.cursor()

    # execute the INSERT statement
    cur.execute(sql, project)

    # commit the changes
    conn.commit()

    # get the id of the last inserted row
    return cur.lastrowid


def add_task(conn, task):
    # insert table statement
    sql = '''INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
             VALUES(?,?,?,?,?,?) '''
    
    # create a cursor
    cur = conn.cursor()

    # execute the INSERT statement
    cur.execute(sql, task)

    # commit the changes
    conn.commit()

    # get the id of the last inserted row
    return cur.lastrowid


def main():
    try:
        with sqlite3.connect('../my.db') as conn:
            # add  a project
            project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
            project_id = add_project(conn, project)
            print(f'Created a project with the id {project_id}')

            # add tasks to the project 
            tasks = [
                ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02'),
                ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
            ]

            for task in tasks:
                task_id = add_task(conn, task)
                print(f'Created task with the id {task_id}')


    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    main()