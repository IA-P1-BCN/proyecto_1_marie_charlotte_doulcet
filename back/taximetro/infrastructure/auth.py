import configparser
import hashlib
import hmac
import secrets

AUTH_SECTION = "auth"
PASSWORD_HASH_KEY = "password_hash"

def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 600_000).hex()
    return f"{salt}${digest}"

def check_password(password, stored_hash):
    salt, _, digest = stored_hash.partition("$")
    expected = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 600_000).hex()
    return hmac.compare_digest(expected, digest)

def is_password_set(path="auth.ini"):
    parser = configparser.ConfigParser()
    if not parser.read(path):
        return False
    return bool(parser.get(AUTH_SECTION, PASSWORD_HASH_KEY, fallback=""))

def save_password_hash(password_hash, path="auth.ini"):
    parser = configparser.ConfigParser()
    parser.read(path)
    if not parser.has_section(AUTH_SECTION):
        parser.add_section(AUTH_SECTION)
    parser.set(AUTH_SECTION, PASSWORD_HASH_KEY, password_hash)
    with open(path, "w") as f:
        parser.write(f)

def load_password_hash(path="auth.ini"):
    parser = configparser.ConfigParser()
    parser.read(path)
    return parser.get(AUTH_SECTION, PASSWORD_HASH_KEY)