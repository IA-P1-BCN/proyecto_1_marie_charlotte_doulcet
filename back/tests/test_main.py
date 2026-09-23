import unittest
from taximetro.main import toggle_state, main
import io
from contextlib import redirect_stdout
from unittest.mock import patch

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
        self.assertAlmostEqual(total, 0.5)  

class TestMainLoop(unittest.TestCase):
    @patch("builtins.input", side_effect=["F", "Q"])
    def test_f_without_active_ride_prints_warning(self, mock_input):
        output = io.StringIO()
        with redirect_stdout(output):
            main()
        self.assertIn("No hay una carrera en curso", output.getvalue())

    @patch("taximetro.main.time.time", side_effect=[1000.0, 1010.0])
    @patch("builtins.input", side_effect=["N", "F", "Q"])
    def test_n_and_f_creates_and_finalizes_ride(self, mock_input, mock_time):
        output = io.StringIO()
        with redirect_stdout(output):
            main()
        self.assertIn("Carrera finalizada. Total a pagar: 0.20", output.getvalue())

    @patch("taximetro.main.time.time", side_effect=[1000.0, 1010.0, 2000.0, 2010.0])
    @patch("builtins.input", side_effect=["N", "F", "N", "F", "Q"])
    def test_second_rule_ride_after_first_ends_has_independent_total(self, mock_input, mock_time):
        output = io.StringIO()
        with redirect_stdout(output):
            main()
        printed = output.getvalue()
        self.assertEqual(printed.count("Carrera finalizada. Total a pagar: 0.20"), 2)

if __name__ == '__main__':
    unittest.main()

