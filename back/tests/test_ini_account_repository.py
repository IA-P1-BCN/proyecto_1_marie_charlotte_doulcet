import os
import tempfile
import unittest
from taximetro.domain.account import Account
from taximetro.infrastructure.ini_account_repository import IniAccountRepository


class TestIniAccountRepository(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(tempfile.mkdtemp(), "auth.ini")
        self.repository = IniAccountRepository(self.path)

    def test_get_returns_none_when_nothing_is_stored(self):
        self.assertIsNone(self.repository.get())

    def test_save_then_get_round_trip(self):
        self.repository.save(Account(company="Taxis Sol", password_hash="salt$digest"))
        self.assertEqual(self.repository.get(), Account(company="Taxis Sol", password_hash="salt$digest"))

    def test_legacy_file_with_only_a_password_hash_has_no_company(self):
        with open(self.path, "w") as f:
            f.write("[auth]\npassword_hash = salt$digest\n")
        account = self.repository.get()
        self.assertEqual(account, Account(company="", password_hash="salt$digest"))
        self.assertFalse(account.is_registered)

    def test_save_replaces_a_previous_account(self):
        self.repository.save(Account(company="Vieja", password_hash="a$b"))
        self.repository.save(Account(company="Nueva", password_hash="c$d"))
        self.assertEqual(self.repository.get(), Account(company="Nueva", password_hash="c$d"))


if __name__ == "__main__":
    unittest.main()
