import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = "data/workout_log.csv"

if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
    print("No workout data found. Run main.py first.")
    exit()

df = pd.read_csv(file_path)

# FIXED COLUMN NAMES (5 columns)
df.columns = ["date", "time", "duration", "jumps", "calories"]

# combine date + time into single datetime
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])

df["date"] = df["datetime"].dt.date

print("\nWORKOUT SUMMARY")
print(f"Total Sessions: {len(df)}")
print(f"Total Jumps: {df['jumps'].sum()}")
print(f"Avg Duration: {df['duration'].mean():.2f}s")
print(f"Total Calories: {df['calories'].sum():.2f}")

daily = df.groupby("date").sum(numeric_only=True)

plt.figure()
plt.plot(daily.index, daily["jumps"])
plt.title("Daily Jumps")

plt.figure()
plt.plot(daily.index, daily["calories"])
plt.title("Daily Calories")

plt.figure()
plt.plot(daily.index, daily["duration"])
plt.title("Daily Duration")

plt.show()