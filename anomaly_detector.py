import pandas as pd


class ModeFlappingDetector:

    def __init__(self, config):

        cfg = config["mode_flapping"]

        self.device_col = cfg["device_column"]
        self.mode_col = cfg["network_mode_column"]

        self.threshold = cfg["max_transitions"]

    def detect(self, df):

        output = df.copy()

        output["Anomaly"] = "No"
        output["Reason"] = ""
        output["Severity"] = "Low"

        grouped = output.groupby(self.device_col)

        for device_id, group in grouped:

            transitions = (
                group[self.mode_col]
                .ne(group[self.mode_col].shift())
                .sum()
            ) - 1

            transitions = max(transitions, 0)

            if transitions >= self.threshold:

                output.loc[group.index, "Anomaly"] = "Yes"

                output.loc[
                    group.index,
                    "Reason"
                ] = (
                    f"{transitions} mode transitions "
                    f"detected for this device"
                )

                output.loc[
                    group.index,
                    "Severity"
                ] = "High"

            else:

                output.loc[
                    group.index,
                    "Reason"
                ] = "Transition count within threshold"

        return output