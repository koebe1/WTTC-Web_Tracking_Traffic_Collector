from __future__ import print_function
import json
import os

# define file path of the file you want to filter
file = '/Users/bene/Desktop/dataset2/captured/create-dataset_local-Storage/create-dataset.com/data.json'
# specify folder you want to save the filtered json file
folder = '/Users/bene/Desktop/dataset2/captured/create-dataset_local-Storage/create-dataset.com'


def filter():
    with open(file, 'r+') as jsonFile:
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

    with open(os.path.join(folder, 'filtered.json'), 'w') as jsonFile:
        json.dump(filtered_list, jsonFile, indent=4)


filter()
