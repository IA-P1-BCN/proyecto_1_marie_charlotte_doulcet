import unittest
from taximetro.main import toggle_state

class TestToogleState(unittest.TestCase):
    def setUp(self):
        self.rates={
            "stopped_rate": 0.02,
            "moving_rate": 0.05}

    def test_toogle_switches_state_and_accumulates_segment(self):
        state, start_timestamp, total = toggle_state(
            "M", "stopped", start_timestamp=1000.0, total=0.0,
            rates=self.rates, now=1010.0
        )
        self.assertEqual(state, "moving")
        self.assertEqual(start_timestamp, 1010.0)
        self.assertAlmostEqual(total, 0.2)

    def test_tooglesame_state_is_noop(self):
        state, start_timestamp, total = toggle_state(
            "M", "moving", start_timestamp=1000.0, total=0.5,
            rates=self.rates, now=1010.0
        )
        self.assertEqual(state, "moving")
        self.assertEqual(start_timestamp, 1000.0)
        self.assertEqual(total, 0.5)

    def test_toggle_to_stopped_accumulates_moving_segment(self):
        state, start_timestamp, total = toggle_state(
            "P", "moving", start_timestamp=1000.0, total=0.0,
            rates=self.rates, now=1010.0
        )
        self.assertEqual(state, "stopped")
        self.assertEqual(start_timestamp, 1010.0)
        self.assertAlmostEqual(total, 0.5)  # 10s en mouvement * 0.05

if __name__ == '__main__':
    unittest.main()


                    