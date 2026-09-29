import unittest
import os
import tempfile

from taximetro.infrastructure.auth import hash_password, check_password, is_password_set, save_password_hash, load_password_hash


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.tmp_dir, "config.ini")

    def test_save_then_load_password_hash_round_trip(self):
        save_password_hash("somesalt$somedigest", self.config_path)
        self.assertEqual(load_password_hash(self.config_path), "somesalt$somedigest")

    def test_hash_then_check_correct_password_succeeds(self):
        password_hash = hash_password("secreto123")
        self.assertTrue(check_password("secreto123", password_hash))

    def test_check_wrong_password_fails(self):
        password_hash = hash_password("secreto123")
        self.assertFalse(check_password("incorrecta", password_hash))

    def test_is_password_set_false_on_fresh_config(self):
        self.assertFalse(is_password_set(self.config_path))


if __name__ == '__main__':
    unittest.main()