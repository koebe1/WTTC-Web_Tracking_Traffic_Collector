import paths
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


# FOLDERS
scripts = paths.scripts
dataset = paths.dataset
dependencies = paths.dependencies
captured = paths.captured


# SCRIPTS
get_ublock_log = paths.get_ublock_log
open_docker = paths.open_docker


# DOCUMENTS
website_txt = f"{dataset}/websites.txt"

# DATA
website_list = []
stripped_website_list = []

with open(os.path.join(dependencies, 'config.yml')) as f:
    config = yaml.safe_load(f)
    num = config["num"]
    max_container_num = config["max_container_num"]
    timeout = config["timeout"]


# FUNCTIONS

# opens websites.txt file and extracts the websites into an array
def get_website_list():

    with open(website_txt) as file:
        content = file.read()
        websites = re.findall(r'(https?://[^\s]+)', content)

    # website_list: [https://example.com,...] stripped_website_list: [example.com,...]
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


#  function for website calls
def call_website(website, port):
    driver = webdriver.Remote(f"http://127.0.0.1:{port}")
    driver.get(website)
    time.sleep(num)

    driver.delete_all_cookies()
    driver.quit()


def collect_data(curr_dir):

    # make copy so real lists dont get manipulated
    websites = website_list.copy()
    stripped_websites = stripped_website_list.copy()
    print("")
    print("Starting containers...")
    print(
        f"                       -> maximal container number set to: {max_container_num}")
    print(
        f"                       -> time to collect web traffic per website set to: {num}s")

    print("")

    ports = []

    # start containers and call websites as long as there are websites in the websites list
    while len(websites) > 0:

        i = 0
        j = i+1
        port_num = 4444

        # restrict number of containers by max_container_num and len(websites)
        while max_container_num > i and i < len(websites):
            # start containers with dynamic names, ports and volumes

            os.system(
                f'docker run --rm -d --name chrome_{j} -p {port_num}:{port_num} --expose={port_num} -v "/{curr_dir}/{stripped_websites[i]}/":/ssl -e SSLKEYLOGFILE=ssl/sslkeylogfile.txt retreatguru/headless-chromedriver chromedriver --port={port_num} --whitelisted-ips=')
            os.system(
                f'docker run --rm -d --name tcpdump_{j} --net=container:chrome_{j} -v /{curr_dir}/{stripped_websites[i]}/:/tcpdump kaazing/tcpdump  not host 127.0.0.1 and not host 172.17.0.1  -v -i any -w  tcpdump/tcpdump.pcap')

            ports.append(port_num)
            port_num += 1
            i += 1
            j += 1

        # define list for processes
        processes = []

        # start as many processes (website calls) as there are containers (i) with different websites and ports
        for _ in range(i):
            p = multiprocessing.Process(target=call_website, args=[
                websites[0], ports[0]])
            p.start()
            processes.append(p)
            # remove first element of websites, stripped_websites and ports as they have already been called/used
            print(
                f"Website {websites[0]} called on port {ports[0]}!")
            websites.pop(0)
            stripped_websites.pop(0)
            ports.pop(0)

        # join processes to continue script if all processes are finished
        for process in processes:
            process.join(timeout)

        os.system("docker kill $(docker ps -q)")


def create_json_and_label_data(curr_dir):
    # get list of subdirectories
    sub_dirs = (next(os.walk(curr_dir))[1])

    print("")
    print("Labeling data...")

    total_blocked_urls_app = 0

    # loop through subdirectories
    for sub_dir in sub_dirs:

        sub_dir_path = os.path.join(captured, curr_dir, sub_dir)

        # change directory to sub_dir
        os.chdir(sub_dir_path)

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
        curr_dir = f"{captured}/{directory}"

        # create folder from user input
        create_folder(curr_dir)

        # create subdirectories
        for stripped in stripped_website_list:

            stripped_path = f"{curr_dir}/{stripped}"

            create_folder(stripped_path)

        # starting uBlock log extraction and open docker simultaneously if docker app is open
        extract = multiprocessing.Process(
            target=extract_ublock_log, args=[curr_dir])

        # get docker_path from config.yml
        with open(os.path.join(dependencies, 'config.yml')) as f:
            config = yaml.safe_load(f)
            docker_path = config["docker_path"]
            docker_startup_time = config["docker_startup_time"]

        # check if docker app is open, if not open app and wait
        if "docker" in (p.name() for p in psutil.process_iter()):
            print("Docker is up and running...")

        # start docker application
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, docker_path])
            print("Starting Docker...")
            time.sleep(docker_startup_time)

        # start uBlock log extraction
        extract.start()
        extract.join()

        # start docker and call the websites
        collect_data(curr_dir)
        create_json_and_label_data(curr_dir)
        print("")
        print("Finsihed!")


main()
