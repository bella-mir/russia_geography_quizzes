import sqlite3


def get_conn():
    conn = sqlite3.connect('rquiz.db')
    return conn

def create_user(username, password_hash):
    conn = get_conn()
    cursor = conn.cursor()
    result = cursor.execute("""INSERT INTO Users([Handle],[Password]) VALUES (?, ?)""", (username,  password_hash))
    conn.commit()
    print(result)

def get_user_by_name(name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Users WHERE Handle = (?)""", (name,))
    columns = [column[0] for column in cursor.description]
    results = []

    for row in cursor:
        d = dict(zip(columns, row))
        results.append(d)
    
    if len(results)>0:
        return results[0]
    else:
        return None
