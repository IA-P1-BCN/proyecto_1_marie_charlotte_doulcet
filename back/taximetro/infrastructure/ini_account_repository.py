import configparser
from taximetro.domain.account import Account
from taximetro.domain.account_repository import AccountRepository

SECTION = "auth"
PASSWORD_HASH_KEY = "password_hash"
COMPANY_KEY = "company"


class IniAccountRepository(AccountRepository):
    """Account stored in auth.ini (git-ignored: it holds the password hash)."""

    def __init__(self, path="auth.ini"):
        self.path = path

    def get(self):
        parser = self._read()
        password_hash = parser.get(SECTION, PASSWORD_HASH_KEY, fallback="")
        if not password_hash:
            return None
        return Account(company=parser.get(SECTION, COMPANY_KEY, fallback=""), password_hash=password_hash)

    def save(self, account):
        parser = self._read()
        if not parser.has_section(SECTION):
            parser.add_section(SECTION)
        parser.set(SECTION, PASSWORD_HASH_KEY, account.password_hash)
        parser.set(SECTION, COMPANY_KEY, account.company)
        with open(self.path, "w") as f:
            parser.write(f)

    def _read(self):
        parser = configparser.ConfigParser()
        parser.read(self.path)
        return parser
