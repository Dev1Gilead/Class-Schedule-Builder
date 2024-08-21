import unittest
from algorithms.schedule_helpers import is_course_offered_in_semester

class TestIsCourseOfferedInSemester(unittest.TestCase):

    def test_course_offered_in_semester(self):
        # Test if a course is correctly identified as being offered in a specific semester
        term = "Fall"
        sub_term = "A"
        course = {
            'terms_offered': 'Fall A, Spring B, Summer',
            'recurrence': 1
        }

        semester = "Fall 2024 A"
        result = is_course_offered_in_semester(course, semester)
        self.assertTrue(result[0])  # Check if the course is offered
        self.assertEqual(result[1], "A")  # Check if the correct sub-term is returned

    def test_course_not_offered_in_semester(self):
        # Test if a course is correctly identified as not being offered in a specific semester
        course = {
            'terms_offered': 'Spring A, Summer B',
            'recurrence': 1
        }

        semester = "Fall 2024 A"
        result = is_course_offered_in_semester(course, semester)
        self.assertFalse(result[0])  # Check that the course is not offered

    def test_course_offered_with_recurrence(self):
        # Test if a course with recurrence is offered in the right semesters
        course = {
            'terms_offered': 'Fall',
            'recurrence': 1
        }

        semester = "Fall 2025"
        result = is_course_offered_in_semester(course, semester)
        self.assertTrue(result[0])  # Check if the course is offered
        self.assertEqual(result[1], "full")  # Check that it's offered for the full semester

    def test_course_offered_in_specific_year(self):
        # Test if a course with a specific year is correctly identified
        course = {
            'terms_offered': 'Fall 2025',
            'recurrence': 1
        }

        semester = "Fall 2025"
        result = is_course_offered_in_semester(course, semester)
        self.assertTrue(result[0])  # Check if the course is offered
        self.assertEqual(result[1], "full")  # Check that it's offered for the full semester

    def test_course_not_offered_in_wrong_year(self):
        # Test if a course is not incorrectly identified in the wrong year
        course = {
            'terms_offered': 'Fall 2025',
            'recurrence': 1
        }

        semester = "Fall 2026"
        result = is_course_offered_in_semester(course, semester)
        self.assertFalse(result[0])  # Check that the course is not offered

if __name__ == '__main__':
    unittest.main()
