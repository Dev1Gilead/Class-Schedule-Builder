import unittest
from models.student import fetch_student_data, fetch_required_courses

class TestStudentFunctions(unittest.TestCase):

    def test_fetch_student_data(self):
        # Test fetching student data
        student_id = 123456
        student = fetch_student_data(student_id)
        
        self.assertIsNotNone(student, "Student data should not be None")
        self.assertEqual(student.student_id, student_id, "Student ID should match")
        self.assertEqual(student.major, "Business", "Major should be 'Business'")

    def test_fetch_required_courses(self):
        # Test fetching required courses
        student_id = 123456
        student = fetch_student_data(student_id)
        print(f"student {student}")

        self.assertIsNotNone(student, "Student data should not be None")

        required_courses = fetch_required_courses(student)
        print(f"student {required_courses}")
        self.assertIsInstance(required_courses, list, "Required courses should be a list")
        self.assertGreater(len(required_courses), 0, "There should be at least one required course")
        
        # Test that the correct courses are fetched
        course_codes = [course['course_code'] for course in required_courses]
        expected_courses = ["BUSN 211", "BUSN 212"]
        for course in expected_courses:
            self.assertIn(course, course_codes, f"{course} should be in the required courses list")

        # Check that course details are correctly fetched
        for course in required_courses:
            self.assertIn('course_code', course, "Course should have a 'course_code'")
            self.assertIn('prerequisites', course, "Course should have 'prerequisites'")
            self.assertIn('terms_offered', course, "Course should have 'terms_offered'")
            self.assertIn('times_offered', course, "Course should have 'times_offered'")

if __name__ == '__main__':
    unittest.main()
