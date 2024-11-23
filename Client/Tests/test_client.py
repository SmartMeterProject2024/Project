import sys
import os
from unittest.mock import call, patch
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from json_converter import convert_to_json
from Client.usage_generator import wait_for_next_interval
from Client.usage_generator import generate_usage

class TestClient(unittest.TestCase):

    def test_convert_to_json(self):
        id = 123
        time = "2024-10-29T21:07:28.484042"
        usage = 45.67
        expected_result = {
            "id": id,
            "time": time,
            "usage": usage
        }
        result = convert_to_json(id, time, usage)
        self.assertEqual(result, expected_result)

    @patch('reading_generator.time.sleep', return_value=None) # the tests mock the time intervals
    @patch('reading_generator.random.randint', side_effect=[15, 30, 40, 50, 60]) # example valid intervals to test
    def test_wait_for_next_interval(self, mock_randint, mock_sleep):
        for _ in range(5):
            wait_for_next_interval()

        self.assertEqual(mock_sleep.call_count, 5)

        intervals = [call[0][0] for call in mock_randint.call_args_list]
        for interval in intervals:
            self.assertTrue(15 <= interval <= 60, "Interval out of range")

    def test_generate_reading(self):
        for _ in range(100):
            number = generate_usage()
            self.assertTrue(isinstance(number, (int, float)), "Reading is not a number")
            self.assertTrue(0 <= number, "Invalid Reading")

if __name__ == '__main__':
    unittest.main(verbosity=2)
