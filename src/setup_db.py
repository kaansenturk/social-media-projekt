import sqlite3

DBNAME = "social_media.db"
def create_tables():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # drop tables if exists
    cur.execute("DROP TABLE IF EXISTS user_data")
    sql = f"CREATE TABLE IF NOT EXISTS user_data (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, zipcode INTEGER, city TEXT, job TEXT, hobbies TEXT)"
    cur.execute(sql)