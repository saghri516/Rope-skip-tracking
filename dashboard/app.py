import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Smart Rope Fitness",
    page_icon="🏋️",
    layout="wide"
)

file_path = "data/workout_log.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
    st.warning("No workout data found! Run main.py first.")
    st.stop()

df = pd.read_csv(file_path)

df.columns = ["date", "time", "duration", "jumps", "calories"]
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
df["date"] = df["datetime"].dt.date

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("⚙️ Filters")

min_date = df["date"].min()
max_date = df["date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

filtered_df = df[
    (df["date"] >= date_range[0]) &
    (df["date"] <= date_range[1])
]

# -----------------------------
# HEADER
# -----------------------------
st.title("🏋️ Smart Rope Fitness Dashboard")
st.markdown("Track your jumps, calories, and progress like a pro athlete.")

# -----------------------------
# KPIS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Sessions", len(filtered_df))
col2.metric("Total Jumps", int(filtered_df["jumps"].sum()))
col3.metric("Avg Duration", f"{filtered_df['duration'].mean():.2f}s")
col4.metric("Calories", f"{filtered_df['calories'].sum():.2f}")

st.divider()

# -----------------------------
# DAILY AGGREGATION
# -----------------------------
daily = filtered_df.groupby("date").sum(numeric_only=True)

# -----------------------------
# CHARTS SECTION
# -----------------------------
st.subheader("📊 Performance Analytics")

chart1, chart2 = st.columns(2)

with chart1:
    fig, ax = plt.subplots()
    ax.plot(daily.index, daily["jumps"], marker="o")
    ax.set_title("Daily Jumps")
    ax.set_xlabel("Date")
    ax.set_ylabel("Jumps")
    st.pyplot(fig)

with chart2:
    fig, ax = plt.subplots()
    ax.plot(daily.index, daily["calories"], marker="o", color="orange")
    ax.set_title("Daily Calories")
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories")
    st.pyplot(fig)

# -----------------------------
# RAW DATA VIEW
# -----------------------------
st.subheader("📁 Workout History")

st.dataframe(
    filtered_df.sort_values("datetime", ascending=False),
    use_container_width=True
)