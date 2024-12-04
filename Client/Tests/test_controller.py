import sys
import os
import unittest
from unittest.mock import Mock, patch

from mvc.usage_model import UsageModel
from mvc.usage_view import UsageView
from mvc.usage_controller import UsageController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestController(unittest.TestCase):
    @patch('mvc.usage_controller.UsageController.update_view')  # Mock the helper_function
    def test_init(self, mock_view_update):
        mock_callback = Mock()
        mock_view = Mock()
        model = UsageModel(0.00, 0.0, 0.00)
        controller = UsageController(model, mock_view, mock_callback)
        self.assertEqual(controller.last_total_usage, model.get_total_usage())
        mock_view_update.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)
