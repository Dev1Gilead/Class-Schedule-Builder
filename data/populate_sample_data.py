import pandas as pd
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('class_scheduler.db')
    conn.row_factory = sqlite3.Row
    return conn

def parse_prerequisites(prereq_string):
    if not isinstance(prereq_string, str) or not prereq_string.strip():
        return []

    # Split by ';' to handle AND conditions
    and_conditions = [item.strip() for item in prereq_string.split(';')]
    
    # For each AND condition, further split by '|' to handle OR conditions
    parsed_prereqs = []
    for condition in and_conditions:
        or_conditions = [course.strip() for course in condition.split('|')]
        parsed_prereqs.append(or_conditions)
    
    return parsed_prereqs

def populate_courses():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Read data from the Excel file
    df = pd.read_excel('data/Classes.xlsx')

    # Insert each row into the courses table, skipping duplicates
    for _, row in df.iterrows():
        try:
            # Parse the prerequisites using the new logic
            parsed_prereqs = parse_prerequisites(row['prerequisites'])

            # Ensure the 'info' field is a string, even if it's empty
            info = row['info'] if pd.notna(row['info']) else ""

            cursor.execute('''
            INSERT INTO courses (course_code, title, terms_offered, times_offered, prerequisites, recurrence, info, credits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (row['course'], row['title'], row['terms_offered'], row['times_offered'], str(parsed_prereqs), row['recurrence'], info, row['credits']))
        except sqlite3.IntegrityError:
            # Handle the case where the course already exists
            print(f"Course {row['course']} already exists, skipping.")

    conn.commit()
    conn.close()

def populate_student_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the first student
    cursor.execute('''
        INSERT OR IGNORE INTO students (student_id, completed_courses, major, minor, expected_graduation)
        VALUES (?, ?, ?, ?, ?)
        ''', ("123456", "BUSN 101,BUSN 205,MATH 190", "Business", None, "Spring 2027"))

    # Insert the second student
    cursor.execute('''
        INSERT OR IGNORE INTO students (student_id, completed_courses, major, minor, expected_graduation)
        VALUES (?, ?, ?, ?, ?)
        ''', ("654321", "CS 101,CS 102", "Business", "None", "Fall 2026"))

    #do not include spaces in the above list of classes taken
    
    conn.commit()
    conn.close()

def verify_student_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students WHERE student_id = ?', ("123456",))
    student = cursor.fetchone()
    conn.close()

    if student:
        print(f"Student with ID {student['student_id']} exists in the database.")
    else:
        print("Student data not found.")

if __name__ == "__main__":
    populate_courses()
    populate_student_data()
    verify_student_data()
