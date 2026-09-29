import sqlite3
from contextlib import closing
from datetime import datetime
from taximetro.domain.ride_record import RideRecord
from taximetro.domain.ride_repository import RideRepository

SCHEMA = """
CREATE TABLE IF NOT EXISTS rides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    ended_at TEXT NOT NULL,
    duration_seconds REAL NOT NULL,
    amount REAL NOT NULL
);
"""
COLUMNS = "id, started_at, ended_at, duration_seconds, amount"


def _to_record(row):
    ride_id, started_at, ended_at, duration_seconds, amount = row
    return RideRecord(
        id=ride_id,
        started_at=datetime.fromisoformat(started_at),
        ended_at=datetime.fromisoformat(ended_at),
        duration_seconds=duration_seconds,
        amount=amount,
    )


class SqliteRideRepository(RideRepository):
    def __init__(self, db_path="taximetro.db"):
        self.db_path = db_path
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute(SCHEMA)

    def save(self, ride):
        record = RideRecord(
            id=None,
            started_at=datetime.fromtimestamp(ride.started_at),
            ended_at=datetime.fromtimestamp(ride.ended_at),
            duration_seconds=ride.get_duration_seconds(),
            amount=round(ride.accumulated, 2),
        )
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            cursor = conn.execute(
                "INSERT INTO rides (started_at, ended_at, duration_seconds, amount) VALUES (?, ?, ?, ?)",
                (record.started_at.isoformat(), record.ended_at.isoformat(), record.duration_seconds, record.amount),
            )
        return RideRecord(cursor.lastrowid, record.started_at, record.ended_at, record.duration_seconds, record.amount)

    def find_by_id(self, ride_id):
        with closing(sqlite3.connect(self.db_path)) as conn:
            row = conn.execute(f"SELECT {COLUMNS} FROM rides WHERE id = ?", (ride_id,)).fetchone()
        return _to_record(row) if row else None

    def find_by_date(self, day):
        with closing(sqlite3.connect(self.db_path)) as conn:
            rows = conn.execute(
                f"SELECT {COLUMNS} FROM rides WHERE started_at LIKE ? ORDER BY id", (f"{day.isoformat()}%",)
            ).fetchall()
        return [_to_record(row) for row in rows]
