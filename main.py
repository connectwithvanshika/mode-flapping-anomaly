import yaml
import pandas as pd

from anomaly_detector import ModeFlappingDetector

with open("config/config.yaml") as file:
    config = yaml.safe_load(file)

detector = ModeFlappingDetector(config)

INPUT_FILE = "data/Telemetry_X_ATP_last7days_20260622.csv.gz"
OUTPUT_FILE = "output/anomaly_report.csv"

CHUNK_SIZE = 200000

first_chunk = True
total_rows = 0
total_anomalies = 0

for chunk in pd.read_csv(
    INPUT_FILE,
    compression="gzip",
    sep="\t",
    chunksize=CHUNK_SIZE,
    low_memory=False
):

    result = detector.detect(chunk)

    anomalies = (result["Anomaly"] == "Yes").sum()

    total_anomalies += anomalies
    total_rows += len(result)

    result.to_csv(
        OUTPUT_FILE,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    first_chunk = False

    print(
        f"Processed {total_rows:,} rows | "
        f"Detected {total_anomalies:,} anomalies"
    )

print("\nFinished")
print(f"Rows Processed: {total_rows:,}")
print(f"Total Anomalies: {total_anomalies:,}")