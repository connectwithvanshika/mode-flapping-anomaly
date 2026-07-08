import yaml
import pandas as pd

from anomaly_detector import ModeFlappingDetector


with open("config/config.yaml") as file:
    config = yaml.safe_load(file)

df = pd.read_csv("data/Telemetry Data.csv")

detector = ModeFlappingDetector(config)

result = detector.detect(df)

result.to_csv(
    "output/anomaly_report.csv",
    index=False
)

print(
    f"Detected {len(result)} mode flapping anomalies."
)