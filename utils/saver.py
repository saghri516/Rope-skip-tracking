import csv
import os
from datetime import datetime

def get_next_session_id(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return 1

    with open(file_path, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

        # remove header
        if len(rows) <= 1:
            return 1

        last_row = rows[-1]

        try:
            return int(last_row[0]) + 1
        except:
            return 1


def save_session(jumps, duration, calories):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    file_path = os.path.join(data_dir, "workout_log.csv")

    os.makedirs(data_dir, exist_ok=True)

    file_exists = os.path.isfile(file_path)
    file_empty = not file_exists or os.path.getsize(file_path) == 0

    session_id = get_next_session_id(file_path)

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time_only = now.strftime("%H:%M:%S")

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)

        # Header
        if file_empty:
            writer.writerow(["SessionID", "Date", "Time", "Duration", "Jumps", "Calories"])

        writer.writerow([
            session_id,
            date,
            time_only,
            round(duration, 2),
            jumps,
            round(calories, 2)
        ])

    print(f"Session {session_id} saved")