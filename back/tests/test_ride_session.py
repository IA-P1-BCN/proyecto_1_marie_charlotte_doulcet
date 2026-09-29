import os
import tempfile
import unittest
from unittest.mock import patch
from taximetro.domain.errors import NoActiveRideError, RideAlreadyActiveError, AlreadyInStateError
from taximetro.domain.rates import Rates
from taximetro.domain.ride_record import RideRecord
from taximetro.domain.ride_state import RideState
from taximetro.infrastructure.sqlite_ride_repository import SqliteRideRepository
from taximetro.ride_session import RideSession


class TestRideSession(unittest.TestCase):
    def setUp(self):
        self.rates = Rates(stopped_rate=0.02, moving_rate=0.05)
        self.repository = SqliteRideRepository(os.path.join(tempfile.mkdtemp(), "test.db"))
        self.session = RideSession(self.rates, self.repository)

    def test_start_ride_with_custom_rates_leaves_defaults_untouched(self):
        custom = Rates(stopped_rate=0.1, moving_rate=0.2)
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
        self.session.change_state(RideState.MOVING)
        self.assertIs(self.session.current_ride.state, RideState.MOVING)

    def test_end_ride_without_active_ride_raises(self):
        with self.assertRaises(NoActiveRideError):
            self.session.end_ride()

    def test_end_ride_saves_clears_current_ride_and_returns_the_record(self):
        self.session.start_ride()
        record = self.session.end_ride()
        self.assertFalse(self.session.has_active_ride)
        self.assertIsInstance(record, RideRecord)
        self.assertEqual(self.session.get_today_history(), [record])

    def test_get_ride_returns_a_saved_record_or_none(self):
        self.session.start_ride()
        record = self.session.end_ride()
        self.assertEqual(self.session.get_ride(record.id), record)
        self.assertIsNone(self.session.get_ride(999))

    @patch("taximetro.ride_session.save_rates")
    def test_change_rate_updates_rates_and_persists(self, mock_save_rates):
        self.session.change_rate("moving_rate", 0.1)
        expected = Rates(stopped_rate=0.02, moving_rate=0.1)
        self.assertEqual(self.session.rates, expected)
        mock_save_rates.assert_called_once_with(expected)

    @patch("taximetro.ride_session.save_rates")
    def test_set_rates_replaces_both_rates_and_persists_once(self, mock_save_rates):
        new_rates = Rates(stopped_rate=0.03, moving_rate=0.06)
        self.session.set_rates(new_rates)
        self.assertEqual(self.session.rates, new_rates)
        mock_save_rates.assert_called_once_with(new_rates)

if __name__ == '__main__':
    unittest.main()