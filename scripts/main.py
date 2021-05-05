import path
import os
import re
import time
import threading
from start_containers import start_container_set_1_2_3, start_container_set_1_2, start_container_set_1, stop_containers
from open_website_1 import call_website_1
from open_website_2 import call_website_2
from open_website_3 import call_website_3

# FOLDERS
scripts = path.scripts
dataset = path.dataset
captured = path.captured
curr_dir = path.curr_dir

# SCRIPTS
get_ublock_log = path.get_ublock_log
open_docker = path.open_docker
start_containers = path.start_containers
open_website_1 = path.open_website_1
open_website_2 = path.open_website_2
open_website_3 = path.open_website_3


# DOCUMENTS
website_txt = "/Users/bene/Desktop/dataset2/websites.txt"

# DATA
website_list = []
stripped_website_list = []


def create_folders():
  # create folder with timestamp
    os.makedirs(curr_dir)

    # create files folder
    files_path = os.path.join(curr_dir, "files")
    os.makedirs(files_path)

    with open(website_txt) as file:
        content = file.read()
        websites = re.findall(r'(https?://[^\s]+)', content)
    # create folder with stripped url as name

    for website in websites:
        website_list.append(website)
        stripped = website.replace("https://", "")
        stripped_website_list.append(stripped)
        os.makedirs(os.path.join(curr_dir, stripped))


# def call_webistes_1_2_3():
#     os.system("python " + open_website_1 + " & " + "python " +
#               open_website_2 + " & " + "python " + open_website_3 + " &")


# def open_website_1_2():
#     os.system("python " + open_website_1 + " & " +
#               "python " + open_website_2 + " &")


# def call_single_website():
#     os.system("python " + open_website_1 + " &")


def collect_data():
    temp = website_list.copy()

    for website in website_list:
        # check how many container to start according to the number of websites to call (max number containers is 3)
        if len(temp) >= 3:
            # start 3 containers
            start_container_set_1_2_3()

            # wait for containers to start up
            time.sleep(16)

            website_1 = temp[0]
            website_2 = temp[1]
            website_3 = temp[2]
            call_website_1(website_1)
            call_website_2(website_2)
            call_website_3(website_3)
            stop_containers()
            print(temp)
            print(temp[0])
            temp.pop(0)
            temp.pop(0)
            temp.pop(0)

        elif len(temp) == 2:
            start_container_set_1_2()
            time.sleep(20)
            stop_containers()
            print(temp)
            print(temp[0])
            temp.pop(0)
            temp.pop(0)

        elif len(temp) == 1:
            start_container_set_1()
            time.sleep(20)
            stop_containers()
            print(temp)
            print(temp[0])
            temp.pop(0)

        elif len(temp) == 0:
            print("done!")
            break


def main():
    create_folders()
    # os.system('python ' + get_ublock_log)
    # os.system('python ' + open_docker)
    collect_data()


main()
