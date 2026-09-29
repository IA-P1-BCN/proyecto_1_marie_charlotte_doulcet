import unittest
from dataclasses import FrozenInstanceError
from taximetro.domain.rates import Rates
from taximetro.domain.ride_state import RideState


class TestRates(unittest.TestCase):
    def setUp(self):
        self.rates = Rates(stopped_rate=0.02, moving_rate=0.05)

    def test_rate_for_returns_the_rate_of_each_state(self):
        self.assertEqual(self.rates.rate_for(RideState.STOPPED), 0.02)
        self.assertEqual(self.rates.rate_for(RideState.MOVING), 0.05)

    def test_rate_for_accepts_the_state_as_a_plain_string(self):
        self.assertEqual(self.rates.rate_for("moving"), 0.05)

    def test_rate_for_unknown_state_raises(self):
        with self.assertRaises(ValueError):
            self.rates.rate_for("flying")

    def test_non_positive_rate_is_rejected(self):
        for bad in (0, -1, -0.01):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Rates(stopped_rate=bad, moving_rate=0.05)

    def test_non_numeric_or_boolean_rate_is_rejected(self):
        for bad in ("0.1", None, True):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Rates(stopped_rate=0.02, moving_rate=bad)

    def test_with_rate_returns_a_new_object_and_leaves_the_original(self):
        updated = self.rates.with_rate("moving_rate", 0.1)
        self.assertEqual(updated, Rates(stopped_rate=0.02, moving_rate=0.1))
        self.assertEqual(self.rates.moving_rate, 0.05)

    def test_with_rate_unknown_key_raises(self):
        with self.assertRaises(ValueError):
            self.rates.with_rate("nope_rate", 0.1)

    def test_rates_are_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.rates.moving_rate = 1.0

    def test_to_dict_uses_the_api_and_config_keys(self):
        self.assertEqual(self.rates.to_dict(), {"stopped_rate": 0.02, "moving_rate": 0.05})


if __name__ == "__main__":
    unittest.main()
