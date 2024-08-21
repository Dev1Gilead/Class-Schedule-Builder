import unittest
from models.student import fetch_student_data, fetch_required_courses
from algorithms.course_sorting import sort_courses

class TestCourseSorting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fetch student data once for all tests
        cls.student_id = 123456  # Replace with a valid student ID in your database
        cls.student = fetch_student_data(cls.student_id)
        cls.courses_to_take = fetch_required_courses(cls.student)

    def test_sort_courses_basic(self):
        
        print(f"Courses to take{self.courses_to_take}\n")

        sorted_courses = sort_courses(self.courses_to_take)
        #print(f"Sorted courses {"\033[31m"}{sorted_courses}{"\033[0m"}")

        sorted_course_codes = [course['course_code'] for course in sorted_courses]
        print(f"Sorted courses codes{"\033[31m"}{sorted_course_codes}{"\033[0m"}")

        # Expected order based on the prerequisite fulfillment scores
        expected_order = ['BUSN 211', 'BUSN 212']  # Adjust according to your database data
        self.assertEqual(sorted_course_codes, expected_order)

if __name__ == '__main__':
    unittest.main()
