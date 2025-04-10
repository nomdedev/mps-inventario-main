import unittest
from mps.config.design_config import DESIGN_CONFIG

class TestDesignConfig(unittest.TestCase):
    def test_design_config_keys(self):
        expected_keys = [
            "primary", "secondary", "background", "text",
            "error", "warning", "success", "border_radius"
        ]
        for key in expected_keys:
            self.assertIn(key, DESIGN_CONFIG)

    def test_design_config_values(self):
        for key, value in DESIGN_CONFIG.items():
            self.assertIsInstance(value, str)
