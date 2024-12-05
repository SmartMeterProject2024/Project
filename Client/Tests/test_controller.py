from datetime import datetime
import sys
import os
import unittest
from unittest.mock import Mock, patch

from mvc.usage_model import UsageModel
from mvc.usage_controller import UsageController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestController(unittest.TestCase):
    # Testing constructor, mocking the view
    @patch('mvc.usage_controller.UsageController.update_view')
    def test_init(self, mock_view_update):
        mock_callback = Mock()
        mock_view = Mock()
        model = UsageModel(0.00, 0.0, 0.00)
        controller = UsageController(model, mock_view, mock_callback)
        self.assertEqual(controller.last_total_usage, model.get_total_usage())
        mock_view_update.assert_called_once()

    # Testing Create Reading, datetime.now is mocked for test consistency
    @patch('mvc.usage_controller.datetime')
    def test_create_reading(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 12, 4, 22, 56, 28)
        mock_callback = Mock()
        mock_view = Mock()
        model = UsageModel(0.00, 0.0, 0.00)
        controller = UsageController(model, mock_view, mock_callback)
        model.set_total_usage(14.00)
        new_reading = controller.create_reading()
        self.assertEqual(new_reading.get_time(), '2024-12-04T22:56:28')
        self.assertEqual(new_reading.get_usage(), 14.00)

if __name__ == '__main__':
    unittest.main(verbosity=2)
