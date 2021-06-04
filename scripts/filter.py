import os
from paths import captured
import json

curr_dir = "/Users/bene/Desktop/dataset2/captured/top5alexa/websites"


def filter(folder):
    with open(f"{folder}/data.json", 'r+') as jsonFile:
        # Transforms json input to python dict
        data = json.load(jsonFile)

    filtered_list = []

    for packet in data:
        if('tcp' in packet['_source']['layers']):
            filtered_list.append({'frame.number': packet['_source']['layers']['frame']['frame.number'],
                                  'tracker': packet['tracker'],
                                  'ip': packet['_source']['layers']['ip'],
                                  'tcp': packet['_source']['layers']['tcp']})

        elif('udp' in packet['_source']['layers']):
            filtered_list.append({'frame.number': packet['_source']['layers']['frame']['frame.number'],
                                  'tracker': packet['tracker'],
                                  'ip': packet['_source']['layers']['ip'],
                                  'udp': packet['_source']['layers']['udp']})

        elif('ip' in packet['_source']['layers']):
            filtered_list.append({'frame.number': packet['_source']['layers']['frame']['frame.number'],
                                  'tracker': packet['tracker'],
                                  'ip': packet['_source']['layers']['ip']})

        else:
            filtered_list.append({'frame.number': packet['_source']['layers']['frame']['frame.number'],
                                  'tracker': packet['tracker']})

    with open(f"{folder}/filtered.json", 'w') as jsonFile:
        json.dump(filtered_list, jsonFile, indent=4)


def total():

    sub_dirs = (next(os.walk(curr_dir))[1])

    for sub_dir in sub_dirs:

        sub_dir_path = f"{curr_dir}/{sub_dir}"
        filter(sub_dir_path)


total()
