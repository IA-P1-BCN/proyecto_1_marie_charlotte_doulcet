import unittest
import os
import tempfile

from taximetro.rates_config import load_rates, save_rates

class TestRatesConfig(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.tmp_dir, "config.ini")

    def _write_config(self, content):
        with open(self.config_path, "w") as f:
            f.write(content)

    def test_load_rates_returns_expected_keys(self):
        self._write_config("[rates]\nstopped_rate = 0.02\nmoving_rate = 0.05\n")
        rates = load_rates(self.config_path)
        self.assertEqual(rates, {"stopped_rate": 0.02, "moving_rate": 0.05})

    def test_missing_key_raises_clear_error(self):
        self._write_config("[rates]\nstopped_rate = 0.02\n")
        with self.assertRaises(ValueError):
            load_rates(self.config_path)

    def test_save_rates_persists_new_values_to_file(self):
        self._write_config("[rates]\nstopped_rate = 0.02\nmoving_rate = 0.05\n")
        save_rates({"stopped_rate": 0.03, "moving_rate": 0.05}, self.config_path)

        reloaded = load_rates(self.config_path)
        self.assertEqual(reloaded, {"stopped_rate": 0.03, "moving_rate": 0.05})

    def test_save_rates_rejects_negative_or_zero(self):
        self._write_config("[rates]\nstopped_rate = 0.02\nmoving_rate = 0.05\n")
        with self.assertRaises(ValueError):
            save_rates({"stopped_rate": -1, "moving_rate": 0.05}, self.config_path)


if __name__ == '__main__':
    unittest.main()