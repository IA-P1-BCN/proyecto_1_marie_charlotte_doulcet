import unittest
import os
from datetime import date
from unittest.mock import patch
from taximetro import history

class TestHistory(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_rides_history.txt"
        self.patcher = patch('taximetro.history.HISTORY_FILE', self.test_file)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_append_then_load_returns_the_ride(self): 
        ride = {"date": date.today().isoformat(), "duration_seconds": "600", "amount": "12.50"}
        history.append_ride(ride)
        rides = history.load_today_rides()
        self.assertEqual(rides, [ride])

    def test_load_today_empty_returns_empty_list(self):
        self.assertEqual(history.load_today_rides(), [])