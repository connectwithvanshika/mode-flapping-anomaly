import pandas as pd


class ModeFlappingDetector:

    def __init__(self, config):
        self.config = config["mode_flapping"]

    def detect(self, df):

        device_col = self.config["device_column"]
        mode_col = self.config["network_mode_column"]

        threshold = self.config["max_transitions"]

        output = df.copy()

        output["Anomaly"] = "No"
        output["Reason"] = "Transition count within threshold"
        output["Severity"] = "Low"

        for device_id, group in output.groupby(device_col):

            transitions = (
                group[mode_col] != group[mode_col].shift()
            ).sum() - 1

            transitions = max(transitions, 0)

            if transitions >= threshold:

                indices = group.index

                output.loc[indices, "Anomaly"] = "Yes"

                output.loc[
                    indices,
                    "Reason"
                ] = (
                    f"{transitions} network mode "
                    f"transitions detected."
                )

                output.loc[
                    indices,
                    "Severity"
                ] = "High"

        return output