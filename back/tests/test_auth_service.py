import unittest
from taximetro.application.auth_service import AuthService
from taximetro.application.token_store import TokenStore
from taximetro.domain.account import Account
from taximetro.domain.errors import AlreadyRegisteredError, BlankCredentialsError, InvalidCredentialsError
from tests.fakes import FakePasswordHasher, InMemoryAccountRepository


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.accounts = InMemoryAccountRepository()
        self.tokens = TokenStore()
        self.service = AuthService(self.accounts, FakePasswordHasher(), self.tokens)

    def test_not_registered_on_fresh_install(self):
        self.assertFalse(self.service.is_registered())

    def test_register_stores_the_account_and_returns_a_valid_token(self):
        token = self.service.register("Taxis Sol", "secreto123")
        self.assertTrue(self.service.is_registered())
        self.assertTrue(self.service.is_valid_token(token))
        self.assertEqual(self.accounts.get(), Account(company="Taxis Sol", password_hash="fake$secreto123"))

    def test_register_twice_raises(self):
        self.service.register("Taxis Sol", "secreto123")
        with self.assertRaises(AlreadyRegisteredError):
            self.service.register("Otra", "otra")

    def test_register_rejects_blank_company_or_password(self):
        for company, password in (("   ", "secreto123"), ("Taxis Sol", "   ")):
            with self.subTest(company=company, password=password):
                with self.assertRaises(BlankCredentialsError):
                    self.service.register(company, password)
        self.assertFalse(self.service.is_registered())

    def test_legacy_password_without_company_is_not_registered_and_gets_replaced(self):
        self.accounts.save(Account(company="", password_hash="fake$vieja"))
        self.assertFalse(self.service.is_registered())
        self.service.register("Taxis Sol", "nueva")
        self.assertEqual(self.accounts.get(), Account(company="Taxis Sol", password_hash="fake$nueva"))

    def test_login_with_correct_credentials_returns_a_valid_token(self):
        self.service.register("Taxis Sol", "secreto123")
        self.assertTrue(self.service.is_valid_token(self.service.login("Taxis Sol", "secreto123")))

    def test_login_ignores_case_and_outer_spaces_of_the_company(self):
        self.service.register("Taxis Sol", "secreto123")
        self.assertTrue(self.service.is_valid_token(self.service.login("  taxis sol ", "secreto123")))

    def test_login_wrong_password_wrong_company_or_unregistered_raises(self):
        with self.assertRaises(InvalidCredentialsError):
            self.service.login("Taxis Sol", "secreto123")
        self.service.register("Taxis Sol", "secreto123")
        for company, password in (("Taxis Sol", "mala"), ("Otra", "secreto123")):
            with self.subTest(company=company):
                with self.assertRaises(InvalidCredentialsError):
                    self.service.login(company, password)

    def test_invalid_token_is_rejected(self):
        self.assertFalse(self.service.is_valid_token("nope"))


if __name__ == "__main__":
    unittest.main()
