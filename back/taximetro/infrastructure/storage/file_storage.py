import csv
import os
from datetime import date
from taximetro.infrastructure.storage.base import Storage
from taximetro.domain.ride import Ride 

class FileStorage(Storage):
    def __init__(self, filepath="rides_history.csv"):
        self.filepath = filepath
        self.fieldnames = ["date", "duration_seconds", "amount"]

    def save_ride(self, ride):
        file_exists = os.path.exists(self.filepath)
        with open(self.filepath, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "date": date.today().isoformat(),
                "duration_seconds": str(ride.get_duration_seconds()),
                "amount": ride.format_total()
            })

    def load_today (self):
        if not os.path.exists(self.filepath):
            return []
        today_str = date.today().isoformat()
        rides = []

        with open(self.filepath, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["date"] == today_str:
                    duration = int(row["duration_seconds"])
                    amount = float(row["amount"])

                    dummy_rates = {"stopped_rate": 0.0, "moving_rate": 0.0}
                    ride = Ride(dummy_rates, started_at=0.0)
                    ride.ended_at = duration  
                    ride.accumulated = amount  

                    rides.append(ride)

        return rides 
