import os
from paths import captured
import json


curr_dir = "/Users/bene/Desktop/dataset2/captured/create-dataset.com"


def average_timestamp(folder, time_relative):
    with open(f"{folder}/data.json", 'r+') as jsonFile:
        # Transforms json input to python dict
        data = json.load(jsonFile)

        for packet in data:
            layers = packet["_source"]["layers"]

            if "tcp" in packet["_source"]["layers"]:
                if "http2" in layers:
                    try:
                        time_relative.append(float(
                            packet["_source"]["layers"]["tcp"]["Timestamps"]["tcp.time_relative"]))
                    except:
                        pass


def total():

    sub_dirs = (next(os.walk(curr_dir))[1])

    sub_dirs.remove("total")
    time_relative = []

    for sub_dir in sub_dirs:

        sub_dir_path = f"{captured}/create-dataset.com/{sub_dir}/create-dataset.com"
        average_timestamp(sub_dir_path, time_relative)

    added = 0

    for entry in time_relative:
        added += entry

    average = added / len(time_relative)
    print(average)


total()
