import unittest
from taximetro.pricing import calculate_segment, format_amount

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

    def test_accumulate_across_2_segments(self):
        rates = {"stopped_rate": 0.02, "moving_rate": 0.05}
        total = calculate_segment("stopped", 10, rates) + calculate_segment("moving", 5, rates)
        self.assertAlmostEqual(total, 0.45)

    def test_total_rounded_to_two_decimals(self):
        result = format_amount(12.3456)
        self.assertEqual(result, "12.35")

if __name__ == '__main__':
    unittest.main()