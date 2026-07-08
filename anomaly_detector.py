import pandas as pd
import yaml


class ModeFlappingDetector:

    def __init__(self, config):
        self.config = config["mode_flapping"]

    def detect(self, df):

        device_col = self.config["device_column"]
        mode_col = self.config["network_mode_column"]

        anomalies = []

        grouped = df.groupby(device_col)

        for device_id, device_data in grouped:

            transitions = (
                device_data[mode_col]
                != device_data[mode_col].shift()
            ).sum() - 1

            transitions = max(transitions, 0)

            if transitions >= self.config["max_transitions"]:

                anomalies.append({
                    "device_id": device_id,
                    "anomaly_type": self.config["anomaly_name"],
                    "severity": self.config["severity"],
                    "transition_count": transitions,
                    "status": "Detected"
                })

        return pd.DataFrame(anomalies)