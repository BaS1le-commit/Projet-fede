import csv
from datetime import datetime
import os

class PresenceLogger:
    def __init__(self, filename="src\Data\presence_log.csv"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Nom", "Date", "Heure"])

    def log_presence(self, name):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, date_str, time_str])
