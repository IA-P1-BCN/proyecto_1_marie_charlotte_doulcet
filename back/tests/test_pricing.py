import unittest
from taximetro.pricing import calculate_segment 

class TestPricing(unittest.TestCase):
    def test_calculate_segment(self):
        rates = {
            'stopped_rate': 0.02,
            'moving_rate': 0.05}
        result = calculate_segment("stopped", 10, rates)
        self.assertEqual(result, 0.2)

    def test_calculate_segment_moving(self):
        rates = {"stopped_rate": 0.02, "moving_rate": 0.05}
        result = calculate_segment("moving", 10, rates)
        self.assertEqual(result, 0.5)
if __name__ == '__main__':
    unittest.main()
    