import sqlite3
from contextlib import closing
from datetime import datetime, date
from taximetro.infrastructure.storage.base import Storage
from taximetro.domain.ride import Ride

SCHEMA = """
CREATE TABLE IF NOT EXISTS rides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    ended_at TEXT NOT NULL,
    duration_seconds REAL NOT NULL,
    amount REAL NOT NULL
);
"""

class DbStorage(Storage):
    def __init__(self, db_path="taximetro.db"):
        self.db_path = db_path
        self.last_inserted_id = None
        with closing(sqlite3.connect(self.db_path)) as conn:
            with conn:
                conn.execute(SCHEMA)

    def save_ride(self, ride):
        started_at = datetime.fromtimestamp(ride.started_at).isoformat()
        ended_at = datetime.fromtimestamp(ride.ended_at).isoformat()
        with closing(sqlite3.connect(self.db_path)) as conn:
            with conn:
                cursor = conn.execute(
                    "INSERT INTO rides (started_at, ended_at, duration_seconds, amount) VALUES (?, ?, ?, ?)",
                    (started_at, ended_at, ride.get_duration_seconds(), round(ride.accumulated, 2)),
                )
                self.last_inserted_id = cursor.lastrowid

    def load_today(self):
        today_str = date.today().isoformat()
        with closing(sqlite3.connect(self.db_path)) as conn:
            rows = conn.execute(
                "SELECT duration_seconds, amount FROM rides WHERE started_at LIKE ?",
                (f"{today_str}%",),
            ).fetchall()

        rides = []
        dummy_rates = {"stopped_rate": 0.0, "moving_rate": 0.0}
        for duration_seconds, amount in rows:
            ride = Ride(dummy_rates, started_at=0.0)
            ride.ended_at = duration_seconds
            ride.accumulated = amount
            rides.append(ride)
        return rides

    def load_by_id(self, ride_id):
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM rides WHERE id = ?", (ride_id,)).fetchone()

    def load_by_date(self, target_date):
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(
                "SELECT * FROM rides WHERE started_at LIKE ?",
                (f"{target_date}%",),
            ).fetchall()
