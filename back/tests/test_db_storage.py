import unittest
import os
import time
from taximetro.infrastructure.storage.db_storage import DbStorage
from taximetro.domain.ride import Ride

class TestDbStorage(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_taximetro.db"
        self.storage = DbStorage(self.test_db)
        self.rates = {"stopped_rate": 0.02, "moving_rate": 0.05}

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_then_load_today_returns_the_ride(self):
        # DbStorage filters "today" from the ride's real started_at (per DB_MODEL.md,
        # unlike FileStorage which stamps date.today() at save time) — timestamps must
        # be real "now"-based, not an arbitrary historical epoch.
        now = time.time()
        ride = Ride(self.rates, started_at=now - 600)
        ride.end(now=now)

        self.storage.save_ride(ride)

        loaded = self.storage.load_today()
        self.assertEqual(len(loaded), 1)
        self.assertAlmostEqual(loaded[0].accumulated, 12.0)

    def test_load_today_empty_db_returns_empty_list(self):
        loaded = self.storage.load_today()
        self.assertEqual(loaded, [])

if __name__ == '__main__':
    unittest.main()
