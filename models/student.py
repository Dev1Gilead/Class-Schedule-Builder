import sqlite3
from data.database import get_db_connection

class Student:
    def __init__(self, student_id, completed_courses, major, minor, expected_graduation):
        self.student_id = student_id
        self.completed_courses = completed_courses
        self.major = major
        self.minor = minor
        self.expected_graduation = expected_graduation

def fetch_student_data(student_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        student_row = cursor.fetchone()

        if student_row:
            # Assuming expected_graduation is stored in the format "Fall 2025" in the database
            expected_graduation = student_row['expected_graduation']
            return Student(
                student_id=student_row['student_id'],
                completed_courses=student_row['completed_courses'],
                major=student_row['major'],
                minor=student_row['minor'],
                expected_graduation=expected_graduation
            )
        return None
    except sqlite3.Error as e:
        print(f"An error occurred while fetching student data: {e}")
        return None
    finally:
        if conn:
            conn.close()

def fetch_required_courses(student):
    completed_courses = student.completed_courses.split(',')
    major = student.major

    # Example logic to determine required courses based on the student's major and what they've completed
    if major == "Business":
        required_courses = ["BUSN 205", "BUSN 211", "BUSN 212", "BUSN 220", "BUSN 230", 
                            "BUSN 319", "BUSN 320", "BUSN 323", "BUSN 328", "BUSN 347", 
                            "BUSN 361", "BUSN 370", "BUSN 376", "BUSN 422", "BUSN 478", 
                            "BBST 103", "BBST 165", "BBST 209", "BBST 210", "BBST 260", 
                            "BBST 306", "ARTS 100", "BIOS 100", "BIOS 121", "COMM 200", 
                            "ENGL 112", "ENGL 220", "ENGL 313", "MATH 190", "MATH 210", 
                            "MUSC 314", "PHIL 210", "POSC 225", "PSYC 200", "SPAN 100", 
                            "SPAN 200"]
  # Adjusted for Business major example
    else:
        required_courses = []  # Add logic for other majors if needed

    # Determine remaining courses by excluding those already completed
    remaining_courses = [course for course in required_courses if course not in completed_courses]

    # Now, fetch details of the remaining courses from the database
    conn = None
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # This allows access by column name
        cursor = conn.cursor()

        # Create a query to fetch only the remaining required courses
        query = 'SELECT course_code, prerequisites, terms_offered, times_offered, recurrence, credits, info FROM courses WHERE course_code IN ({})'.format(
            ','.join('?' * len(remaining_courses))
        )
        cursor.execute(query, remaining_courses)
        courses = cursor.fetchall()

        # Convert sqlite3.Row objects to dictionaries
        courses = [dict(row) for row in courses]

        return courses

    except sqlite3.Error as e:
        print(f"An error occurred while fetching required courses: {e}")
        return []
    finally:
        if conn:
            conn.close()
