import unittest
from algorithms.generate_schedule import generate_schedule

class TestPreferredTimesOnly(unittest.TestCase):

    def test_preferred_times_only(self):
        # Scenario: Preferred times but no preferred days
        student_id = '123456'
        preferences = {
            'preferred_days': [],
            'preferred_times': ['14:00-18:00']
        }

        final_schedule, unscheduled_courses = generate_schedule(student_id, preferences)

        self.assertIsInstance(final_schedule, dict)
        self.assertIsInstance(unscheduled_courses, list)
        self.assertGreater(len(final_schedule), 0)

        # Check that all scheduled courses fall within the preferred times
        for course, term_time in final_schedule.items():
            term_time = term_time.strip()
            if '(' in term_time and ')' in term_time:
                term, times_offered = term_time.split(' (')
                times_offered = times_offered.rstrip(')')
            else:
                term = term_time
                times_offered = ''

            if times_offered.lower() != 'pending':
                start_time, end_time = map(int, times_offered.replace(':', '').split('-'))
                for preferred_time in preferences['preferred_times']:
                    pref_start, pref_end = map(int, preferred_time.replace(':', '').split('-'))
                    self.assertTrue(pref_start <= end_time and pref_end >= start_time)

if __name__ == '__main__':
    unittest.main()
