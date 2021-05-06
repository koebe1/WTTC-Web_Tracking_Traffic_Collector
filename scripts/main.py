import path
import os
import re
import time
import yaml
import shutil
import datetime
from selenium import webdriver
import multiprocessing


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
# curr_dir = os.path.join(
#     captured, datetime.datetime.now().strftime('%d_%m_%Y %H_%M_%S'))


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

#  MORGEN WEITERMACHEN FOLDER COUNT FUNKTIONIERT NICHT RICHTIG -> BRICHT NACH EXP 1 AB ORDNER ZU ERSTELLEN


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print('Error creating folder:' + e)


def create_folders(directory):
    curr_dir = os.path.join(captured, directory)
    # create folder with timestamp
    create_folder(curr_dir)

    # create ublock_log folder
    ublock_log_path = os.path.join(curr_dir, "ublock_log")
    create_folder(ublock_log_path)

    for stripped in stripped_website_list:
        s = os.path.join(curr_dir, stripped)
        create_folder(s)


# manage DOCKER COMPOSE

def start_container_set_1_2_3():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=all docker-compose up --detach &")


def stop_containers():
    os.chdir("../dependencies")
    os.system("docker compose stop")
    # os.system("docker compose down")


def start_container_set_1_2():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=container-set-1-2 docker-compose up  --detach&")


def start_container_set_1():
    os.chdir("../dependencies")
    os.system("COMPOSE_PROFILES=container-set-1 docker-compose up --detach &")


# manage WEBSITE CALLS
with open(os.path.join(dependencies, 'config.yml')) as f:
    config = yaml.safe_load(f)
    num = config["num"]


def call_website_1(website_1, curr_dir):
    driver_1 = webdriver.Remote('http://127.0.0.1:4444')

    driver_1.get(website_1)
    time.sleep(num)

    stripped = website_1.replace("https://", "")
    shutil.move(os.path.join(dataset, "sslkeylogfile_1.txt"),
                os.path.join(curr_dir, stripped))
    shutil.move(os.path.join(dataset, "tcpdump_1.pcap"),
                os.path.join(curr_dir, stripped))

    # driver_1.delete_all_cookies()
    driver_1.close()
    driver_1.quit()


def call_website_2(website_2, curr_dir):
    driver_2 = webdriver.Remote('http://127.0.0.1:4445')

    driver_2.get(website_2)
    time.sleep(num)

    stripped = website_2.replace("https://", "")
    shutil.move(os.path.join(dataset, "sslkeylogfile_2.txt"),
                os.path.join(curr_dir, stripped))
    shutil.move(os.path.join(dataset, "tcpdump_2.pcap"),
                os.path.join(curr_dir, stripped))

    # driver_2.delete_all_cookies()
    driver_2.close()
    driver_2.quit()


def call_website_3(website_3, curr_dir):
    driver_3 = webdriver.Remote('http://127.0.0.1:4446')
    driver_3.get(website_3)

    time.sleep(num)

    stripped = website_3.replace("https://", "")
    shutil.move(os.path.join(dataset, "sslkeylogfile_3.txt"),
                os.path.join(curr_dir, stripped))
    shutil.move(os.path.join(dataset, "tcpdump_3.pcap"),
                os.path.join(curr_dir, stripped))

    # driver_1.delete_all_cookies()
    driver_3.close()
    driver_3.quit()


# manage PARALLEL CALLS
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
        c1.terminate()
        c2.terminate()
        c3.terminate()


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
        c1.terminate()
        c2.terminate()


# def call_parallel_1(website_1, curr_dir):

#     # call websites simultaneously
#     c1 = multiprocessing.Process(
#         target=call_website_1, args=[website_1, curr_dir])

#     if __name__ == "__main__":
#         c1.start()
#         c1.join()
#         c1.terminate()


def collect_data(curr_dir):
    temp = website_list.copy()

    # check how many container to start according to the number of websites to call (max number containers is 3)
    while len(temp) > 0:
        if len(temp) >= 3:

            # start 3 containers
            start_container_set_1_2_3()

            # wait for containers to start up
            time.sleep(12)

            # get next websites to call
            website_1 = temp[0]
            website_2 = temp[1]
            website_3 = temp[2]

            call_parallel_3(website_1, website_2, website_3, curr_dir)

            print("LEFT THE CALL PARALLEL 3")

            stop_containers()
            # remove websites from copied list temp
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)

        elif len(temp) == 2:
            start_container_set_1_2()

            # wait for containers to start up
            time.sleep(12)

            # get next websites to call
            website_1 = temp[0]
            website_2 = temp[1]

            # call websites parralel
            call_parallel_2(website_1, website_2, curr_dir)

            print("LEFT CALL PARRALEL 2")

            stop_containers()

            temp.pop(0)
            temp.pop(0)

        elif len(temp) == 1:
            start_container_set_1()

            # wait for containers to start up
            time.sleep(12)

            # get next websites to call
            website_1 = temp[0]

            # call websites parralel
            call_website_1(website_1, curr_dir)

            print("LEFT CALL PARRALEL 1")

            stop_containers()

            temp.pop(0)

    print("done")


def main():

    if __name__ == "__main__":

        # create folder system
        directory = input("Enter a directory name:")
        curr_dir = os.path.join(captured, directory)

        # create folder from user input
        create_folder(curr_dir)

        # create ublock_log folder
        ublock_log_path = os.path.join(curr_dir, "ublock_log")
        create_folder(ublock_log_path)

        for stripped in stripped_website_list:
            stripped_path = os.path.join(curr_dir, stripped)
            create_folder(stripped_path)

        # start docker and call the websites
        collect_data(curr_dir)


main()
