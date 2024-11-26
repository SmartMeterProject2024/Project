import sys
import os
from unittest.mock import Mock, call, patch
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reading import Reading
from json_converter import convert_to_json
from usage_generator import wait_for_next_interval
from usage_generator import generate_usage

class TestClient(unittest.TestCase):

    def test_reading_to_json(self):
        id = 123
        time = "2024-10-29T21:07:28.484042"
        usage = 45.67
        new_reading = Reading(time, usage)

        expected_result = {
            "id": id,
            "time": time,
            "usage": usage
        }

        result = convert_to_json(id, new_reading)
        self.assertEqual(result, expected_result)

    @patch('usage_generator.time.sleep', return_value=None) # mock the time intervals
    def test_wait_for_next_interval(self, mock_sleep):
        mock_callback = Mock()
        for _ in range(5):
            wait_for_next_interval(callback=mock_callback)

        # check if called 5 times
        self.assertEqual(mock_sleep.call_count, 5)
        self.assertEqual(mock_callback.call_count, 5)

        # check generated intervals are in range
        intervals = [call[0][0] for call in mock_callback.call_args_list]
        for interval in intervals:
            self.assertTrue(15 <= interval <= 60, "Interval out of range")

    def test_generate_usage(self):
        for _ in range(100):
            usage = generate_usage()
            self.assertTrue(isinstance(usage, (float)), "Reading is not a number")
            self.assertTrue(0 <= usage, "Invalid Reading")
            self.assertTrue(len(str(usage).split('.')[1]) == 1, "Does not have one decimal place")

if __name__ == '__main__':
    unittest.main(verbosity=2)
