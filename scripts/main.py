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
curr_dir = os.path.join(
    captured, datetime.datetime.now().strftime('%d_%m_%Y %H_%M_%S'))

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


def create_folders():
    try:
        # create folder with timestamp
        # os.makedirs(curr_dir, exist_ok=True)
        dir_num = str(sum(os.path.isdir(i) for i in os.listdir(captured)))
        directory = os.path.join(captured, "exp. " + dir_num)
        os.makedirs(directory)

        # create ublock_log folder
        ublock_log_path = os.path.join(directory, "ublock_log")
        os.makedirs(ublock_log_path, exist_ok=True)

        for stripped in stripped_website_list:
            os.makedirs(os.path.join(directory, stripped))

    except OSError as e:
        if e.errno != 17:
            print("Error:", e)


create_folders()
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


def call_website_1(website_1):
    driver1 = webdriver.Remote('http://127.0.0.1:4444')

    driver1.get(website_1)
    time.sleep(num)

    stripped = website_1.replace("https://", "")
    shutil.move(os.path.join(dataset, "sslkeylogfile_1.txt"),
                os.path.join(curr_dir, stripped))
    shutil.move(os.path.join(dataset, "tcpdump_1.pcap"),
                os.path.join(curr_dir, stripped))

    # driver1.delete_all_cookies()
    driver1.close()
    driver1.quit()


def call_website_2(website_2):
    driver1 = webdriver.Remote('http://127.0.0.1:4445')

    driver1.get(website_2)
    time.sleep(num)

    stripped = website_2.replace("https://", "")
    shutil.move(os.path.join(dataset, "sslkeylogfile_2.txt"),
                os.path.join(curr_dir, stripped))
    shutil.move(os.path.join(dataset, "tcpdump_2.pcap"),
                os.path.join(curr_dir, stripped))

    # driver1.delete_all_cookies()
    driver1.close()
    driver1.quit()


def call_website_3(website_3):
    driver1 = webdriver.Remote('http://127.0.0.1:4446')
    driver1.get(website_3)

    time.sleep(num)

    stripped = website_3.replace("https://", "")
    shutil.move(os.path.join(dataset, "sslkeylogfile_3.txt"),
                os.path.join(curr_dir, stripped))
    shutil.move(os.path.join(dataset, "tcpdump_3.pcap"),
                os.path.join(curr_dir, stripped))

    # driver1.delete_all_cookies()
    driver1.close()
    driver1.quit()


# manage PARALLEL CALLS
def call_parallel(website_1, website_2, website_3):

    # call websites simultaneously
    c1 = multiprocessing.Process(
        target=call_website_1, args=[website_1])

    c2 = multiprocessing.Process(
        target=call_website_2, args=[website_2])
    c3 = multiprocessing.Process(
        target=call_website_3, args=[website_3])

    if __name__ == "__main__":

        c1.start()
        c2.start()
        c3.start()
        c1.join()
        c2.join()
        c3.join()


def collect_data():
    temp = website_list.copy()

    for website in website_list:
        print("test")
        # check how many container to start according to the number of websites to call (max number containers is 3)
        if len(temp) >= 3:
            # start 3 containers
            start_container_set_1_2_3()

            # wait for containers to start up
            time.sleep(12)

            # get next websites to call
            website_1 = temp[0]
            website_2 = temp[1]
            website_3 = temp[2]

            call_parallel(website_1, website_2, website_3)
            time.sleep(10)
            stop_containers()
            # remove websites from copied list temp
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


# main()


# create_folders()

# website_1 = website_list[0]
# website_2 = website_list[1]
# website_3 = website_list[2]

# call_parallel(website_1, website_2, website_3)
