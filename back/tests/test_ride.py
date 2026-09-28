
import unittest
from taximetro.domain.ride import Ride

class TestRide(unittest.TestCase):
    def setUp(self):
        self.rates = {
            'stopped_rate': 0.02,
            'moving_rate': 0.05
        }

    def test_new_ride_starts_stopped_with_zero_total(self):
        ride = Ride(self.rates, started_at=1000.0)
        self.assertEqual(ride.state, "stopped")
        self.assertEqual(ride.started_at, 1000.0)
        self.assertEqual(ride.get_total(now=1000.0), 0.0)

    def test_get_total_accumulates_time_in_stopped_state(self):
        ride = Ride(self.rates, started_at=1000.0)
        total = ride.get_total(now=1010.0)
        self.assertAlmostEqual(total, 0.2)

    def test_toggle_to_moving_closes_stopped_segment(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.toggle_state("moving", now=1010.0)
        self.assertEqual(ride.state, "moving")
        self.assertAlmostEqual(ride.accumulated, 0.2)

    def test_toggle_same_state_is_noop(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.toggle_state("stopped", now=1010.0)
        self.assertEqual(ride.state, "stopped")
        self.assertEqual(ride.accumulated, 0.0)

    def test_end_ride_closes_final_segment_and_marks_ended(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.toggle_state("moving", now=1010.0)
        total = ride.end(now=1015.0)
        self.assertAlmostEqual(total, 0.45)
        self.assertEqual(ride.ended_at, 1015.0)

    def test_format_amount_rounds_to_two_decimals(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.accumulated = 12.3456
        formatted = ride.format_total()
        self.assertEqual(formatted, "12.35")

if __name__ == '__main__':
    unittest.main()