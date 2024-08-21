import unittest
from algorithms.generate_schedule import generate_schedule

class TestPreferredDaysAndTimes(unittest.TestCase):

    def test_both_preferred_days_and_times(self):
        # Scenario: Both preferred days and times are provided
        student_id = '123456'
        preferences = {
            'preferred_days': ['Monday', 'Wednesday'],
            'preferred_times': ['14:00-18:00']
        }

        final_schedule, unscheduled_courses = generate_schedule(student_id, preferences)

        self.assertIsInstance(final_schedule, dict)
        self.assertIsInstance(unscheduled_courses, list)
        self.assertGreater(len(final_schedule), 0)

        # Check that all scheduled courses fall on the preferred days and within the preferred times
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

                start_time, end_time = map(int, times_offered.replace(':', '').split('-'))
                for preferred_time in preferences['preferred_times']:
                    pref_start, pref_end = map(int, preferred_time.replace(':', '').split('-'))
                    self.assertTrue(pref_start <= end_time and pref_end >= start_time)

if __name__ == '__main__':
    unittest.main()
