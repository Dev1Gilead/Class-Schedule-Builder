import unittest
from data.database import get_db_connection, create_tables
from data.populate_sample_data import populate_courses

class TestDataInsertion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure tables are created before running tests
        create_tables()

    def test_populate_courses(self):
        # Populate the courses table
        populate_courses()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses;")
        courses = cursor.fetchall()
        conn.close()

        # Check that courses were inserted
        self.assertGreater(len(courses), 0)  # Ensure there is at least one course in the table

        # Optionally, print the courses to inspect them
        for course in courses:
            print(course)

        # Additional checks for the new columns
        for course in courses:
            self.assertIn('credits', course.keys())
            self.assertIn('recurrence', course.keys())
            self.assertIn('info', course.keys())
            self.assertGreaterEqual(int(course['credits']), 0)  # Check that credits are non-negative
            self.assertGreaterEqual(int(course['recurrence']), 1)  # Check that recurrence is at least 1
            self.assertIsInstance(course['info'], str)  # Check that info is a string

if __name__ == '__main__':
    unittest.main()
