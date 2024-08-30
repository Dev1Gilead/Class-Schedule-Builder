import unittest
from algorithms.generate_schedule import generate_schedule
from models.student import fetch_student_data

class TestGenerateSchedule(unittest.TestCase):
    
    def test_generate_schedule_simple(self):
        # Example student ID (this should match a student in your database)
        student_id = '123456'
        
        # Example preferences (no specific preferences for this simple test)
        preferences = {
            'preferred_days': [],
            'preferred_times': [],
            'expected_graduation': 'Spring 2027'
        }
        
        # Fetch the student data to ensure the student exists
        student = fetch_student_data(student_id)
        self.assertIsNotNone(student, "Student should exist in the database")
        
        # Generate the schedule
        final_schedule, unscheduled_courses = generate_schedule(student_id, preferences)
        
        # Assert that the schedule is not empty
        self.assertGreater(len(final_schedule), 0, "Final schedule should contain courses")
        
        # Optionally, print the final schedule for inspection
        print("Final Schedule:", final_schedule)
        print("Unscheduled Courses:", unscheduled_courses)

if __name__ == '__main__':
    unittest.main()
