import hashlib
import hmac
import secrets

ITERATIONS = 600_000


class Pbkdf2PasswordHasher:
    """Salted PBKDF2-HMAC-SHA256. Stored format: `<salt hex>$<digest hex>`."""

    def hash(self, password):
        salt = secrets.token_hex(16)
        return f"{salt}${self._digest(password, salt)}"

    def verify(self, password, stored_hash):
        if not self._is_well_formed(stored_hash):
            return False
        salt, _, digest = stored_hash.partition("$")
        return hmac.compare_digest(self._digest(password, salt), digest)

    @staticmethod
    def _is_well_formed(stored_hash):
        salt, separator, digest = stored_hash.partition("$")
        try:
            bytes.fromhex(salt)
        except ValueError:
            return False
        return bool(separator and salt and digest)

    @staticmethod
    def _digest(password, salt):
        return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), ITERATIONS).hex()
