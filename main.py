import pandas as pd
from anomaly_detector import detect_mode_flapping


df = pd.read_csv("data/telecom_data.csv")

flag, transitions = detect_mode_flapping(df)

if flag:
    print("MODE FLAPPING DETECTED")
    print("Transitions:", transitions)

else:
    print("No anomaly detected")