import unittest
from taximetro.domain.rates import Rates
from taximetro.domain.ride import Ride
from taximetro.domain.ride_state import RideState


class TestRide(unittest.TestCase):
    def setUp(self):
        self.rates = Rates(stopped_rate=0.02, moving_rate=0.05)

    def test_new_ride_starts_stopped_with_zero_total(self):
        ride = Ride(self.rates, started_at=1000.0)
        self.assertIs(ride.state, RideState.STOPPED)
        self.assertEqual(ride.started_at, 1000.0)
        self.assertEqual(ride.get_total(now=1000.0), 0.0)

    def test_state_still_compares_equal_to_its_string_value(self):
        self.assertEqual(Ride(self.rates).state, "stopped")

    def test_get_total_accumulates_time_in_stopped_state(self):
        ride = Ride(self.rates, started_at=1000.0)
        self.assertAlmostEqual(ride.get_total(now=1010.0), 0.2)

    def test_toggle_to_moving_closes_stopped_segment(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.toggle_state(RideState.MOVING, now=1010.0)
        self.assertIs(ride.state, RideState.MOVING)
        self.assertAlmostEqual(ride.accumulated, 0.2)

    def test_toggle_accepts_the_state_as_a_plain_string(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.toggle_state("moving", now=1010.0)
        self.assertIs(ride.state, RideState.MOVING)

    def test_toggle_to_unknown_state_raises(self):
        ride = Ride(self.rates, started_at=1000.0)
        with self.assertRaises(ValueError):
            ride.toggle_state("flying", now=1010.0)

    def test_toggle_same_state_is_noop(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.toggle_state(RideState.STOPPED, now=1010.0)
        self.assertIs(ride.state, RideState.STOPPED)
        self.assertEqual(ride.accumulated, 0.0)

    def test_end_ride_closes_final_segment_and_marks_ended(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.toggle_state(RideState.MOVING, now=1010.0)
        total = ride.end(now=1015.0)
        self.assertAlmostEqual(total, 0.45)
        self.assertEqual(ride.ended_at, 1015.0)

    def test_duration_is_zero_until_the_ride_ends_then_rounded_seconds(self):
        ride = Ride(self.rates, started_at=1000.0)
        self.assertEqual(ride.get_duration_seconds(), 0)
        ride.end(now=1015.4)
        self.assertEqual(ride.get_duration_seconds(), 15)


if __name__ == "__main__":
    unittest.main()
