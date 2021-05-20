import matplotlib.pyplot as plt
import pandas as pd
import json


total = pd.read_json(
    "/Users/bene/Desktop/dataset2/captured/TOTAL_create-dataset/total_filtered.json")


def plot_packet_length():
    with open("/Users/bene/Desktop/dataset2/captured/TOTAL_create-dataset/total_filtered.json", 'r+') as file:
        # Transforms json input to python objects
        data = json.load(file)

    ip_len = []

    for packet in data:
        if "ip" in packet:
            ip_len.append(int(packet['ip']['ip.len']))

    ip_len.sort()
    xy = {}

    for entry in ip_len:
        if entry not in xy:
            xy[entry] = ip_len.count(entry)

    x = xy.keys()
    y = xy.values()
    # x = [1, 2, 3, 4]
    # y = [4, 3, 2, 1]
    plt.plot(x, y, color=(0.235, 0.39, 0.58))
    plt.ylabel('Anzahl Datenpakete')
    plt.xlabel('Länge der Datenpakete')
    plt.title('Verteilung der Datenpaketlänge')
    plt.show()


# plot_packet_length()


def plot_packet_length_google():
    with open("/Users/bene/Desktop/dataset2/captured/TOTAL_create-dataset/total_filtered.json", 'r+') as file:
        # Transforms json input to python objects
        data = json.load(file)

    ip_len = []

    for packet in data:
        if "ip" in packet and "true" in packet["tracker"]:
            ip_len.append(int(packet['ip']['ip.len']))

    ip_len.sort()

    xy = {}

    for entry in ip_len:
        if entry not in xy:
            xy[entry] = ip_len.count(entry)

    # x = xy.keys()
    # y = xy.values()
    # # x = [1, 2, 3, 4]
    # # y = [4, 3, 2, 1]
    # plt.plot(x, y, color=(0.235, 0.39, 0.58))
    # plt.ylabel('Anzahl Datenpakete')
    # plt.xlabel('Länge der Datenpakete')
    # plt.title('Verteilung der Datenpaketlänge')
    # plt.show()


# plot_packet_length_google()


def plot_destination_ip():
    with open("/Users/bene/Desktop/dataset2/captured/TOTAL_create-dataset/total_filtered.json", 'r+') as file:
        # Transforms json input to python objects
        data = json.load(file)

    destination_ip = []

    for packet in data:
        if "ip" in packet:
            destination_ip.append(packet['ip']['ip.dst'])

    # print(destination_ip)

    xy = {}

    for entry in destination_ip:
        if entry not in xy:
            xy[entry] = destination_ip.count(entry)

    print(xy)

    x = xy.keys()
    y = xy.values()

    plt.plot(x, y, color=(0.235, 0.39, 0.58))
    plt.ylabel('Anzahl Datenpakete')
    plt.xlabel('Länge der Datenpakete')
    plt.title('Verteilung der Datenpaketlänge')
    plt.show()


plot_destination_ip()
