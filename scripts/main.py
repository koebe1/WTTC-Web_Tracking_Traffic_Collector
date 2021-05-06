import path
import os
import re
import time
import yaml
import shutil
import datetime
from selenium import webdriver
import multiprocessing
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


def collect_data(curr_dir):
    temp = website_list.copy()

    # check how many container to start according to the number of websites to call (max number containers is 3)
    while len(temp) > 0:
        if len(temp) >= 5:

            # start 3 containers
            start_container_set_5()

            # wait for containers to start up
            time.sleep(20)

            # get next websites to call
            website_1 = temp[0]
            website_2 = temp[1]
            website_3 = temp[2]
            website_4 = temp[3]
            website_5 = temp[4]

            call_parallel_5(website_1, website_2, website_3,
                            website_4, website_5, curr_dir)

            print("LEFT THE CALL PARALLEL 3")

            stop_containers()
            # remove websites from copied list temp
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)

        if len(temp) >= 3:

            # start 3 containers
            start_container_set_3()

            # wait for containers to start up
            time.sleep(10)

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
            start_container_set_2()

            # wait for containers to start up
            time.sleep(10)

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
            time.sleep(10)

            # get next websites to call
            website_1 = temp[0]

            # call websites parralel
            call_website_1(website_1, curr_dir)

            print("LEFT CALL PARRALEL 1")

            stop_containers()

            temp.pop(0)

    print("done!")


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
