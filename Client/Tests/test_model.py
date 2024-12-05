import sys
import os
import unittest

from mvc.usage_model import UsageModel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestModel(unittest.TestCase):
    # Testing constructor
    def test_init(self):
        model = UsageModel(2.00, 3.50, 2.99)
        self.assertEqual(model.get_current_usage(), 2.00)
        self.assertEqual(model.get_total_usage(), 3.50)
        self.assertEqual(model.get_bill(), 2.99)

    # Testing Setter methods
    def test_setters(self):
        model = UsageModel(2.00, 3.50, 2.99)
        model.set_current_usage(12.00)
        model.set_total_usage(18.10)
        model.set_bill(3.90)
        self.assertEqual(model.get_current_usage(), 12.00)
        self.assertEqual(model.get_total_usage(), 18.10)
        self.assertEqual(model.get_bill(), 3.90)

if __name__ == '__main__':
    unittest.main(verbosity=2)
