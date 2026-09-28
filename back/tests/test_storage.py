import unittest
import os
from datetime import date
from taximetro.infrastructure.storage.file_storage import FileStorage
from taximetro.domain.ride import Ride

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_rides_history_refactor.csv"
        self.storage = FileStorage(self.test_file)
        self.rates = {"stopped_rate": 0.02, "moving_rate": 0.05}

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_ride_then_load_today_returns_it(self):
        ride = Ride(self.rates, started_at=1000.0)
        ride.end(now=1600.0)

        self.storage.save_ride(ride)

        loaded = self.storage.load_today()
        self.assertEqual(len(loaded), 1)
        # On vérifie le montant, pas started_at (le CSV ne le sauvegarde pas)
        self.assertAlmostEqual(loaded[0].accumulated, 12.0)

    def test_load_today_empty_file_returns_empty_list(self):
        loaded = self.storage.load_today()
        self.assertEqual(loaded, [])

if __name__ == '__main__':
    unittest.main()