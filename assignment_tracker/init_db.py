"""Run once to create the SQLite database and tables."""

# import os and sqlite3
import os
import sqlite3


"""  To ensure TA/Prof (or anyone) can safetly use we imported os to find the path to database.db
    Although /database.db will always be in our present directory we thought it would be safer to
    add into our program just as a safety precaution
"""
DATABASE = os.path.join(os.path.dirname(__file__), "database.db")


def init_db():
    # connect and open database and intilize a cursor.
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # create basic user table with id being primary key and username being unique
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    """)

    # create an assingments table with id (assignments) being primary, and user_id as foreign key 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            course TEXT DEFAULT '',
            due_date TEXT NOT NULL,
            priority TEXT DEFAULT 'Medium',
            completed INTEGER DEFAULT 0,
            time_studied INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    conn.commit()
    conn.close()
    print(f"Database initialised at {DATABASE}")


if __name__ == "__main__":
    init_db()
