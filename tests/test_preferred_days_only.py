import unittest
from algorithms.generate_schedule import generate_schedule

class TestPreferredDaysOnly(unittest.TestCase):

    def test_preferred_days_only(self):
        # Scenario: Preferred days but no preferred times
        student_id = '123456'
        preferences = {
            'preferred_days': ['Monday', 'Wednesday', 'Friday'],
            'preferred_times': []
        }

        final_schedule, unscheduled_courses = generate_schedule(student_id, preferences)

        self.assertIsInstance(final_schedule, dict)
        self.assertIsInstance(unscheduled_courses, list)
        self.assertGreater(len(final_schedule), 0)

        # Check that all scheduled courses fall on the preferred days
        for course, term_time in final_schedule.items():
            term_time = term_time.strip()
            if '(' in term_time and ')' in term_time:
                term, times_offered = term_time.split(' (')
                times_offered = times_offered.rstrip(')')
            else:
                term = term_time
                times_offered = ''
            
            if times_offered.lower() != 'pending':
                self.assertTrue(any(day in term for day in preferences['preferred_days']))

if __name__ == '__main__':
    unittest.main()
