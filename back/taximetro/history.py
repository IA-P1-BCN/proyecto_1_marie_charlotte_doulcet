import csv 
import os 
from datetime import date

HISTORY_FILE = "rides_history.csv"
FIELDNAMES = ["date", "duration_seconds", "amount"]

def append_ride(ride):
    file_exists = os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(ride)

def load_today_rides():
    if not os.path.exists(HISTORY_FILE):
        return []
    today = date.today().isoformat()
    with open(HISTORY_FILE, newline="") as f: 
        reader = csv.DictReader(f)
        return [row for row in reader if row["date"] == today]