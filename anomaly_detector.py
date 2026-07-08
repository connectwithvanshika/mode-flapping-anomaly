import pandas as pd


def detect_mode_flapping(df,
                          mode_column="NetworkMode",
                          threshold=4):

    transitions = 0
    previous_mode = None

    for mode in df[mode_column]:

        if previous_mode is not None and mode != previous_mode:
            transitions += 1

        previous_mode = mode

    return transitions >= threshold, transitions