import unittest
from algorithms.generate_schedule import generate_schedule

class TestNoCoursesAvailable(unittest.TestCase):

    def test_no_courses_available(self):
        # Edge case: Courses should still be scheduled if they are available in the term,
        # even if the times are "Pending".
        student_id = '123456'
        preferences = {
            'preferred_days': ['Monday'],
            'preferred_times': ['10:00-12:00']
        }

        final_schedule, unscheduled_courses = generate_schedule(student_id, preferences)

        # Check that the schedule includes courses even if times are "Pending"
        self.assertGreater(len(final_schedule), 0)

        # Verify that all scheduled courses have "Pending" times
        for course_code, term_time in final_schedule.items():
            term, times_offered = term_time.split(' (')
            times_offered = times_offered.rstrip(')')
            self.assertEqual(times_offered, 'Pending')

if __name__ == '__main__':
    unittest.main()
