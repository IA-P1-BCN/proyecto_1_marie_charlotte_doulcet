import hmac
from taximetro.domain.account import Account
from taximetro.domain.errors import AlreadyRegisteredError, BlankCredentialsError, InvalidCredentialsError


def _normalize(company):
    return company.strip().casefold()


class AuthService:
    """Single-account authentication for the web panel: company + password, session token."""

    def __init__(self, accounts, hasher, tokens):
        self._accounts = accounts
        self._hasher = hasher
        self._tokens = tokens

    def is_registered(self):
        account = self._accounts.get()
        return account is not None and account.is_registered

    def register(self, company, password):
        if self.is_registered():
            raise AlreadyRegisteredError()
        company, password = company.strip(), password.strip()
        if not company or not password:
            raise BlankCredentialsError()
        # Also replaces a password created earlier from the CLI/GUI (same account).
        self._accounts.save(Account(company=company, password_hash=self._hasher.hash(password)))
        return self._tokens.issue()

    def login(self, company, password):
        account = self._accounts.get()
        if account is None or not account.is_registered:
            raise InvalidCredentialsError()
        password_ok = self._hasher.verify(password.strip(), account.password_hash)
        company_ok = hmac.compare_digest(_normalize(company).encode(), _normalize(account.company).encode())
        if not (company_ok and password_ok):
            raise InvalidCredentialsError()
        return self._tokens.issue()

    def is_valid_token(self, token):
        return self._tokens.is_valid(token)
