import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from json_converter import convert_to_json

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

if __name__ == '__main__':
    unittest.main()
