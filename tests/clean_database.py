import sys
import os

# Adjust the Python path to include the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.database import get_db_connection

def clear_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear the courses table if it exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='courses';")
    if cursor.fetchone():
        cursor.execute('DELETE FROM courses')

    # Clear the students table if it exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students';")
    if cursor.fetchone():
        cursor.execute('DELETE FROM students')

    conn.commit()
    conn.close()

def drop_courses_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS courses')

    conn.commit()
    conn.close()

def drop_students_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS students')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    drop_courses_table()  # Drop courses table first
    drop_students_table()  # Drop students table next
    clear_tables()  # Clear tables in case they weren't dropped
    print("Database tables cleared and dropped where applicable.")
