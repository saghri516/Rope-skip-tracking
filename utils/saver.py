import csv
import os
from datetime import datetime

def save_session(jumps, duration, calories):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    file_path = os.path.join(data_dir, "workout_log.csv")

    os.makedirs(data_dir, exist_ok=True)

    file_exists = os.path.isfile(file_path)

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time_only = now.strftime("%H:%M:%S")

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Time", "Duration", "Jumps", "Calories"])

        writer.writerow([
            date,
            time_only,
            round(duration, 2),
            jumps,
            round(calories, 2)
        ])

    print("Session saved")