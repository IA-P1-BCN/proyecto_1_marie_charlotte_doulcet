import unittest
from taximetro.infrastructure.pbkdf2_password_hasher import Pbkdf2PasswordHasher


class TestPbkdf2PasswordHasher(unittest.TestCase):
    def setUp(self):
        self.hasher = Pbkdf2PasswordHasher()

    def test_hash_then_verify_correct_password_succeeds(self):
        self.assertTrue(self.hasher.verify("secreto123", self.hasher.hash("secreto123")))

    def test_verify_wrong_password_fails(self):
        self.assertFalse(self.hasher.verify("incorrecta", self.hasher.hash("secreto123")))

    def test_same_password_hashes_differently_thanks_to_the_salt(self):
        self.assertNotEqual(self.hasher.hash("secreto123"), self.hasher.hash("secreto123"))

    def test_is_valid_hash_rejects_malformed_values(self):
        self.assertTrue(self.hasher.is_valid_hash(self.hasher.hash("x")))
        self.assertFalse(self.hasher.is_valid_hash("not-a-hash"))
        self.assertFalse(self.hasher.is_valid_hash(""))

    def test_verify_malformed_hash_is_false_instead_of_crashing(self):
        self.assertFalse(self.hasher.verify("x", "not-a-hash"))


if __name__ == "__main__":
    unittest.main()
