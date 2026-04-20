from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()

file_path = "data/workout_log.csv"


@app.get("/stats")
def stats():
    if not os.path.exists(file_path):
        return {"error": "No data"}

    df = pd.read_csv(file_path)
    df.columns = ["date", "time", "duration", "jumps", "calories"]

    return {
        "sessions": len(df),
        "total_jumps": int(df["jumps"].sum()),
        "total_calories": float(df["calories"].sum()),
        "avg_duration": float(df["duration"].mean())
    }


@app.get("/data")
def get_data():
    if not os.path.exists(file_path):
        return {"error": "No data"}

    df = pd.read_csv(file_path)
    df.columns = ["date", "time", "duration", "jumps", "calories"]

    return df.to_dict(orient="records")