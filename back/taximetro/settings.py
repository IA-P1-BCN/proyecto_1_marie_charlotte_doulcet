from pathlib import Path

# Relative paths resolve against the working directory (run everything from back/).
RATES_PATH = "config.ini"
AUTH_PATH = "auth.ini"
DB_PATH = "taximetro.db"

FRONT_DIST = Path(__file__).resolve().parent.parent.parent / "front" / "dist"
