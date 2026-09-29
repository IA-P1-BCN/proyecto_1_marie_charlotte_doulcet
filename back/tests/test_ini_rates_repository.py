import os
import tempfile
import unittest
from taximetro.domain.rates import Rates
from taximetro.infrastructure.ini_rates_repository import IniRatesRepository


class TestIniRatesRepository(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(tempfile.mkdtemp(), "config.ini")
        self.repository = IniRatesRepository(self.path)

    def _write_config(self, content):
        with open(self.path, "w") as f:
            f.write(content)

    def test_load_returns_the_configured_rates(self):
        self._write_config("[rates]\nstopped_rate = 0.02\nmoving_rate = 0.05\n")
        self.assertEqual(self.repository.load(), Rates(stopped_rate=0.02, moving_rate=0.05))

    def test_load_missing_file_raises_clear_error(self):
        with self.assertRaises(ValueError):
            self.repository.load()

    def test_load_missing_key_raises_clear_error(self):
        self._write_config("[rates]\nstopped_rate = 0.02\n")
        with self.assertRaises(ValueError):
            self.repository.load()

    def test_load_rejects_non_positive_values(self):
        self._write_config("[rates]\nstopped_rate = -1\nmoving_rate = 0.05\n")
        with self.assertRaises(ValueError):
            self.repository.load()

    def test_save_then_load_round_trip(self):
        self._write_config("[rates]\nstopped_rate = 0.02\nmoving_rate = 0.05\n")
        self.repository.save(Rates(stopped_rate=0.03, moving_rate=0.06))
        self.assertEqual(self.repository.load(), Rates(stopped_rate=0.03, moving_rate=0.06))

    def test_save_creates_the_file_when_missing(self):
        self.repository.save(Rates(stopped_rate=0.03, moving_rate=0.06))
        self.assertEqual(self.repository.load(), Rates(stopped_rate=0.03, moving_rate=0.06))


if __name__ == "__main__":
    unittest.main()
