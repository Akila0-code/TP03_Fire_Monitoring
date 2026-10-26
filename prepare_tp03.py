
import pandas as pd
import numpy as np
from pathlib import Path

# Correct data folder
data_dir = Path(r"F:\TP02_Big_Data\data")
input_file = data_dir / "big_synthetic.csv"
output_file = data_dir / "tp03_fire_monitoring_sample.csv"

if not input_file.exists():
    raise FileNotFoundError(f"Input file not found: {input_file}")

# Read a small sample to protect RAM
df = pd.read_csv(input_file, nrows=10000)

rng = np.random.default_rng(42)
n = len(df)

# Create synthetic monitoring data
df["timestamp"] = pd.date_range(
    start="2026-01-01 08:00:00",
    periods=n,
    freq="min"
)

df["sensor_id"] = [
    f"SENSOR_{i % 10 + 1:02d}" for i in range(n)
]

df["temperature"] = rng.uniform(18, 42, n).round(1)
df["humidity"] = rng.uniform(20, 85, n).round(1)
df["smoke_level"] = rng.uniform(0, 200, n).round(1)

# Educational simulation rule, not a real fire detection system
df["fire_alarm"] = (
    (df["temperature"] >= 35) &
    (df["smoke_level"] >= 150)
).astype(int)

df["sensor_status"] = np.where(
    df["fire_alarm"] == 1,
    "ALARM",
    "NORMAL"
)

columns = [
    "timestamp",
    "sensor_id",
    "temperature",
    "humidity",
    "smoke_level",
    "fire_alarm",
    "sensor_status"
]

df[columns].to_csv(output_file, index=False)

print("TP03 dataset created successfully")
print("Output:", output_file)
print("Rows:", len(df))
print("Columns:", len(columns))
print("\nAlarm distribution:")
print(df["fire_alarm"].value_counts())
print("\nPreview:")
print(df[columns].head())
