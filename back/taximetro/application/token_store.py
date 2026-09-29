import secrets


class TokenStore:
    """In-memory session tokens, lost on restart. ponytail: persist/expire them if that ever matters."""

    def __init__(self):
        self._tokens = set()

    def issue(self):
        token = secrets.token_urlsafe(32)
        self._tokens.add(token)
        return token

    def is_valid(self, token):
        return token in self._tokens
