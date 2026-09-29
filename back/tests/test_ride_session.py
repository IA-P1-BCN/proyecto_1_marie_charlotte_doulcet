import unittest
import os
from unittest.mock import patch
from taximetro.ride_session import (
    RideSession,
    NoActiveRideError,
    RideAlreadyActiveError,
    AlreadyInStateError,
)
from taximetro.infrastructure.storage.file_storage import FileStorage


class TestRideSession(unittest.TestCase):
    def setUp(self):
        self.rates = {"stopped_rate": 0.02, "moving_rate": 0.05}
        self.test_file = "test_ride_session_history.csv"
        self.storage = FileStorage(self.test_file)
        self.session = RideSession(self.rates, self.storage)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_start_ride_with_custom_rates_leaves_defaults_untouched(self):
        custom = {"stopped_rate": 0.1, "moving_rate": 0.2}
        ride = self.session.start_ride(custom)
        self.assertEqual(ride.rates, custom)
        self.assertNotEqual(self.session.rates, custom)

    def test_start_ride_sets_current_ride(self):
        ride = self.session.start_ride()
        self.assertIs(self.session.current_ride, ride)
        self.assertTrue(self.session.has_active_ride)

    def test_start_ride_twice_raises(self):
        self.session.start_ride()
        with self.assertRaises(RideAlreadyActiveError):
            self.session.start_ride()

    def test_change_state_without_active_ride_raises(self):
        with self.assertRaises(NoActiveRideError):
            self.session.change_state("moving")

    def test_change_state_to_same_state_raises(self):
        self.session.start_ride()
        with self.assertRaises(AlreadyInStateError):
            self.session.change_state("stopped")

    def test_change_state_to_different_state_succeeds(self):
        self.session.start_ride()
        self.session.change_state("moving")
        self.assertEqual(self.session.current_ride.state, "moving")

    def test_end_ride_without_active_ride_raises(self):
        with self.assertRaises(NoActiveRideError):
            self.session.end_ride()

    def test_end_ride_saves_and_clears_current_ride(self):
        self.session.start_ride()
        self.session.end_ride()
        self.assertFalse(self.session.has_active_ride)
        self.assertEqual(len(self.storage.load_today()), 1)

    @patch("taximetro.ride_session.save_rates")
    def test_change_rate_updates_rates_and_persists(self, mock_save_rates):
        self.session.change_rate("moving_rate", 0.1)
        self.assertEqual(self.session.rates["moving_rate"], 0.1)
        mock_save_rates.assert_called_once_with({"stopped_rate": 0.02, "moving_rate": 0.1})

if __name__ == '__main__':
    unittest.main()