import sqlite3

def get_db_connection():
    conn = sqlite3.connect('class_scheduler.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the courses table with updated columns for terms_offered, times_offered, recurrence, info, and credits
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        course_code TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        terms_offered TEXT NOT NULL,
        times_offered TEXT NOT NULL,
        prerequisites TEXT,
        recurrence INTEGER NOT NULL,
        info TEXT,
        credits INTEGER NOT NULL
    )
    ''')

    # Create the students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        completed_courses TEXT,
        major TEXT,
        minor TEXT,
        expected_graduation TEXT
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
