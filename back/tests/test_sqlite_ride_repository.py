import os
import tempfile
import time
import unittest
from datetime import date, datetime
from taximetro.domain.rates import Rates
from taximetro.domain.ride import Ride
from taximetro.domain.ride_record import RideRecord
from taximetro.infrastructure.sqlite_ride_repository import SqliteRideRepository


class TestSqliteRideRepository(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.repository = SqliteRideRepository(os.path.join(self.tmp_dir, "test.db"))
        self.rates = Rates(stopped_rate=0.02, moving_rate=0.05)

    def _finished_ride(self, seconds=600, ended_at=None):
        now = ended_at if ended_at is not None else time.time()
        ride = Ride(self.rates, started_at=now - seconds)
        ride.end(now=now)
        return ride

    def test_save_returns_a_record_with_its_generated_id(self):
        record = self.repository.save(self._finished_ride())

        self.assertIsInstance(record, RideRecord)
        self.assertEqual(record.id, 1)
        self.assertAlmostEqual(record.amount, 12.0)
        self.assertEqual(record.duration_seconds, 600)
        self.assertIsInstance(record.started_at, datetime)
        self.assertEqual((record.ended_at - record.started_at).total_seconds(), 600)

    def test_ids_increment(self):
        first = self.repository.save(self._finished_ride())
        second = self.repository.save(self._finished_ride())
        self.assertEqual((first.id, second.id), (1, 2))

    def test_find_by_id_returns_the_saved_record(self):
        saved = self.repository.save(self._finished_ride())
        self.assertEqual(self.repository.find_by_id(saved.id), saved)

    def test_find_by_id_unknown_returns_none(self):
        self.assertIsNone(self.repository.find_by_id(999))

    def test_find_by_date_returns_only_that_days_rides(self):
        today = self.repository.save(self._finished_ride())
        old = datetime(2020, 1, 2, 10, 0).timestamp()
        self.repository.save(self._finished_ride(ended_at=old))

        self.assertEqual(self.repository.find_by_date(date.today()), [today])
        self.assertEqual(len(self.repository.find_by_date(date(2020, 1, 2))), 1)

    def test_find_by_date_empty_returns_empty_list(self):
        self.assertEqual(self.repository.find_by_date(date.today()), [])


if __name__ == "__main__":
    unittest.main()
