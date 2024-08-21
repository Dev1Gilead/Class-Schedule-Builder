import unittest
from algorithms.utils import is_time_slot_compatible

class TestUtils(unittest.TestCase):

    def test_is_time_slot_compatible(self):
        preferences = {
            "preferred_days": ["Monday", "Wednesday", "Friday"],
            "preferred_times": ["14:00-18:00"],  # Prefers afternoon classes
        }
        self.assertTrue(is_time_slot_compatible("MWF 14:00-15:00", preferences))
        self.assertFalse(is_time_slot_compatible("MWF 08:00-09:00", preferences))

if __name__ == '__main__':
    unittest.main()
