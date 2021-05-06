from selenium import webdriver
import os
import time
import yaml
import path
import shutil


scripts = path.scripts
dataset = path.dataset
dependencies = path.dependencies

with open(os.path.join(dependencies, 'config.yml')) as f:
    config = yaml.safe_load(f)
    num = config["num"]


def call_website_1(website_1, curr_dir):
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

    # driver_3.delete_all_cookies()
    driver_3.close()
    driver_3.quit()


def call_website_4(website_4, curr_dir):
    driver_4 = webdriver.Remote('http://127.0.0.1:4447')

    driver_4.get(website_4)
    time.sleep(num)

    stripped = website_4.replace("https://", "")
    shutil.move(os.path.join(dataset, "sslkeylogfile_4.txt"),
                os.path.join(curr_dir, stripped))
    shutil.move(os.path.join(dataset, "tcpdump_4.pcap"),
                os.path.join(curr_dir, stripped))

    # driver_3.delete_all_cookies()
    driver_4.close()
    driver_4.quit()


def call_website_5(website_5, curr_dir):
    driver_5 = webdriver.Remote('http://127.0.0.1:4448')

    driver_5.get(website_5)
    time.sleep(num)

    stripped = website_5.replace("https://", "")
    shutil.move(os.path.join(dataset, "sslkeylogfile_5.txt"),
                os.path.join(curr_dir, stripped))
    shutil.move(os.path.join(dataset, "tcpdump_5.pcap"),
                os.path.join(curr_dir, stripped))

    # driver_3.delete_all_cookies()
    driver_5.close()
    driver_5.quit()
