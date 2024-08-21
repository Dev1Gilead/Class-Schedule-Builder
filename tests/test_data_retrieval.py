import unittest
from data.database import get_db_connection, create_tables
from data.populate_sample_data import populate_courses

class TestDataRetrieval(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure tables are created and populated before running tests
        create_tables()
        populate_courses()

    def test_retrieve_courses(self):
        # Establish a connection to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve all courses
        cursor.execute("SELECT * FROM courses;")
        courses = cursor.fetchall()

        conn.close()

        # Check that we retrieved some courses
        self.assertGreater(len(courses), 0)  # Ensure that at least one course is retrieved

        # Optionally, you can add checks for specific courses or course attributes
        first_course = courses[0]
        self.assertIn('course_code', first_course.keys())
        self.assertIn('title', first_course.keys())
        self.assertIn('time_slots', first_course.keys())
        self.assertIn('prerequisites', first_course.keys())

if __name__ == '__main__':
    unittest.main()
