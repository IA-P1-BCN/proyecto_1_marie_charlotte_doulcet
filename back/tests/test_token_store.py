import unittest
from taximetro.application.token_store import TokenStore


class TestTokenStore(unittest.TestCase):
    def test_issued_token_is_valid_and_unique(self):
        store = TokenStore()
        first, second = store.issue(), store.issue()
        self.assertNotEqual(first, second)
        self.assertTrue(store.is_valid(first))
        self.assertTrue(store.is_valid(second))

    def test_unknown_or_empty_token_is_invalid(self):
        store = TokenStore()
        self.assertFalse(store.is_valid("nope"))
        self.assertFalse(store.is_valid(""))


if __name__ == "__main__":
    unittest.main()
