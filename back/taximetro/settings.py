from pathlib import Path

RATES_PATH = "config.ini"
AUTH_PATH = "auth.ini"
DB_PATH = "taximetro.db"
LOG_PATH = "taximetro.log"

FRONT_DIST = Path(__file__).resolve().parent.parent.parent / "front" / "dist"
