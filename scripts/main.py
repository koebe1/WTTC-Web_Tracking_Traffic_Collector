import path
import os
import re
import time
import yaml
import shutil
import datetime
import subprocess
import sys
import psutil
from selenium import webdriver
import multiprocessing
from write_statistics import write_statistic, extract_url_ublock
from label import label_data
from open_docker import open_docker_app
from get_ublock_log import extract_ublock_log
from website_calls import call_website_1, call_website_2, call_website_3, call_website_4, call_website_5
from start_containers import stop_containers, start_container_set_1, start_container_set_2, start_container_set_3, start_container_set_5

# FOLDERS
scripts = path.scripts
dataset = path.dataset
dependencies = path.dependencies
captured = path.captured
# curr_dir = path.curr_dir

# SCRIPTS
get_ublock_log = path.get_ublock_log
open_docker = path.open_docker


# DOCUMENTS
website_txt = "/Users/bene/Desktop/dataset2/websites.txt"

# DATA
website_list = []
stripped_website_list = []


# FUNCTIONS

def get_website_list():

    with open(website_txt) as file:
        content = file.read()
        websites = re.findall(r'(https?://[^\s]+)', content)

    for website in websites:
        website_list.append(website)
        stripped = website.replace("https://", "")
        stripped_website_list.append(stripped)

    return website_list, stripped_website_list


l = get_website_list()
website_list = l[0]
stripped_website_list = l[1]


# function to create folders for folder system in application directory


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print('Error creating folder:' + e)


# manage PARALLEL CALLS
def call_parallel_5(website_1, website_2, website_3, website_4, website_5, curr_dir):

    # call websites simultaneously
    c1 = multiprocessing.Process(
        target=call_website_1, args=[website_1, curr_dir])

    c2 = multiprocessing.Process(
        target=call_website_2, args=[website_2, curr_dir])
    c3 = multiprocessing.Process(
        target=call_website_3, args=[website_3, curr_dir])

    c4 = multiprocessing.Process(
        target=call_website_4, args=[website_4, curr_dir])

    c5 = multiprocessing.Process(
        target=call_website_5, args=[website_5, curr_dir])

    if __name__ == "__main__":
        c1.start()
        c2.start()
        c3.start()
        c4.start()
        c5.start()
        c1.join()
        c2.join()
        c3.join()
        c4.join()
        c5.join()


def call_parallel_3(website_1, website_2, website_3, curr_dir):

    # call websites simultaneously
    c1 = multiprocessing.Process(
        target=call_website_1, args=[website_1, curr_dir])

    c2 = multiprocessing.Process(
        target=call_website_2, args=[website_2, curr_dir])
    c3 = multiprocessing.Process(
        target=call_website_3, args=[website_3, curr_dir])

    if __name__ == "__main__":
        c1.start()
        c2.start()
        c3.start()
        c1.join()
        c2.join()
        c3.join()


def call_parallel_2(website_1, website_2, curr_dir):

    # call websites simultaneously
    c1 = multiprocessing.Process(
        target=call_website_1, args=[website_1, curr_dir])

    c2 = multiprocessing.Process(
        target=call_website_2, args=[website_2, curr_dir])

    if __name__ == "__main__":
        c1.start()
        c2.start()
        c1.join()
        c2.join()


def call_parallel_1(website_1, curr_dir):

    # call websites simultaneously
    c1 = multiprocessing.Process(
        target=call_website_1, args=[website_1, curr_dir])

    if __name__ == "__main__":
        c1.start()
        c1.join()


def collect_data(curr_dir):
    temp = website_list.copy()

    # check how many container to start according to the number of websites to call (max number containers is 3)
    while len(temp) > 0:
        print("Starting to collect web traffic...")

        # 5 chrome containers
        if len(temp) >= 5:

            # start 3 containers
            start_container_set_5()

            # wait for containers to start up
            time.sleep(15)

            # get next websites to call
            website_1 = temp[0]
            website_2 = temp[1]
            website_3 = temp[2]
            website_4 = temp[3]
            website_5 = temp[4]

            call_parallel_5(website_1, website_2, website_3,
                            website_4, website_5, curr_dir)

            stop_containers()
            time.sleep(1)
            # remove websites from copied list temp
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)

        # 3 chrome containers
        elif len(temp) < 5 and len(temp) >= 3:

            # start 3 containers
            start_container_set_3()

            # wait for containers to start up
            time.sleep(15)

            # get next websites to call
            website_1 = temp[0]
            website_2 = temp[1]
            website_3 = temp[2]

            call_parallel_3(website_1, website_2, website_3, curr_dir)

            time.sleep(1)
            stop_containers()
            # remove websites from copied list temp
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)

        # 2 chrome containers
        elif len(temp) < 3 and len(temp) >= 2:
            start_container_set_2()

            # wait for containers to start up
            time.sleep(10)

            # get next websites to call
            website_1 = temp[0]
            website_2 = temp[1]

            # call websites parralel
            call_parallel_2(website_1, website_2, curr_dir)

            time.sleep(1)
            stop_containers()

            temp.pop(0)
            temp.pop(0)

        # 1 chrome containers
        elif len(temp) == 1:
            start_container_set_1()

            # wait for containers to start up
            time.sleep(10)

            # get next websites to call
            website_1 = temp[0]

            # call websites parralel
            call_parallel_1(website_1, curr_dir)

            time.sleep(1)
            stop_containers()

            temp.pop(0)


def create_json_and_label_data(curr_dir):
    # get list of subdirectories
    sub_dirs = (next(os.walk(curr_dir))[1])

    print("Creating JSON and labeling data...")

    total_blocked_urls_app = 0

    # loop through subdirectories
    for sub_dir in sub_dirs:

        sub_dir_path = os.path.join(captured, curr_dir, sub_dir)

        # change directory to sub_dir
        os.chdir(sub_dir_path)

        # loop throuh current directory
        for file in os.listdir('.'):
            if re.match('tcpdump', file):
                os.rename(file, "tcpdump.pcap")

            elif re.match('sslkeylogfile', file):
                os.rename(file, "sslkeylogfile.txt")

        ssl_path = os.path.join(
            captured, curr_dir, sub_dir, "sslkeylogfile.txt")

        # create json file from tcpdump.pcap file
        os.system(
            f"tshark -r tcpdump.pcap -T json > data.json -o tls.keylog_file:{ssl_path} --no-duplicate-keys")

        # label data packets
        label_data(curr_dir, sub_dir)
        # write statistics for captured data

        # add up number of blocked elements by the application
        t = write_statistic(curr_dir, sub_dir)
        total_blocked_urls_app += t

        extracted = extract_url_ublock(curr_dir, sub_dir)

        total_blocked_urls_ublock = extracted[0]
        # blocked_urls_ublock = extracted[1]

        s = open(os.path.join(captured, curr_dir, "total_statistics.txt"), "w+")
        s.write(
            f"Blocked URLS:     Application:   {total_blocked_urls_app}       Ublock:   {total_blocked_urls_ublock}")


def main():

    if __name__ == "__main__":

        # create folder system
        directory = input("Enter a directory name:")
        curr_dir = os.path.join(captured, directory)

        # create folder from user input
        create_folder(curr_dir)

        # create ublock_log folder
        # ublock_log_path = os.path.join(curr_dir, "ublock_log")
        # create_folder(ublock_log_path)

        for stripped in stripped_website_list:
            stripped_path = os.path.join(curr_dir, stripped)
            create_folder(stripped_path)

        # starting uBlock log extraction and open docker simultaneously if docker app is open
        extract = multiprocessing.Process(
            target=extract_ublock_log, args=[curr_dir])

        with open(os.path.join(dependencies, 'config.yml')) as f:
            config = yaml.safe_load(f)
            docker_path = config["docker_path"]

        # check if docker app is open, if not open app and wait
        if "docker" in (p.name() for p in psutil.process_iter()):
            print("Docker is up and running...")

        # start docker application
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, docker_path])
            print("Starting Docker...")
            time.sleep(20)

        # start uBlock log extraction
        extract.start()
        extract.join()

        # start docker and call the websites
        collect_data(curr_dir)
        create_json_and_label_data(curr_dir)
        print("Finsihed!")


main()


# AUTOMATISIERTE MARKIERUNG DER DATENPAKETE
# Schleife durch alle Ordner außer ublock (evtl nur ublocklog file speichern und nicht ordner)
# in jedem ordner automatische markierung ?
# ODER alle files zusammenfügen und dann auswerten?
