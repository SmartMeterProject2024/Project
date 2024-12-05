import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reading import Reading

class TestReading(unittest.TestCase):
    # Testing constructor
    def test_init(self):
        reading_A = Reading("2024-10-29T21:07:28.484042", 11.89)
        self.assertEqual(reading_A.get_time(), "2024-10-29T21:07:28.484042")
        self.assertEqual(reading_A.get_usage(), 11.89)

        reading_B = Reading("2024-11-03T21:07:28.484042", 9.23)
        self.assertEqual(reading_B.get_time(), "2024-11-03T21:07:28.484042")
        self.assertEqual(reading_B.get_usage(), 9.23)

if __name__ == '__main__':
    unittest.main(verbosity=2)
