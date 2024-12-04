import sys
import os
from unittest.mock import patch
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generator.usage_generator import UsageGenerator

class TestGenerator(unittest.TestCase):

    @patch('generator.usage_generator.time.sleep', return_value=None) # mock the time intervals
    @patch('builtins.print')  # mock the print function
    def test_wait_for_next_interval(self, mock_print, mock_sleep):
        usage_generator = UsageGenerator()
        for _ in range(5):
            usage_generator.wait_for_next_interval()

        # check if called 5 times
        self.assertEqual(mock_sleep.call_count, 5)
        self.assertEqual(mock_print.call_count, 5)

        # check generated intervals are in range
        intervals = [call[0][0] for call in mock_sleep.call_args_list]
        for interval in intervals:
            self.assertTrue(15 <= interval <= 60, "Interval out of range")

    def test_generate_usage(self):
        usage_generator = UsageGenerator()
        for _ in range(100):
            usage = usage_generator.generate_usage()
            self.assertTrue(isinstance(usage, (float)), "Reading is not a number")
            self.assertTrue(0 <= usage, "Invalid Reading")
            self.assertTrue(len(str(usage).split('.')[1]) == 1 or len(str(usage).split('.')[1]) == 2, "Does not have one or two decimal places")

if __name__ == '__main__':
    unittest.main(verbosity=2)
