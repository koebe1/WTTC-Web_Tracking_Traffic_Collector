from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
import yaml
import path
import re
import shutil



scripts = path.scripts
dataset = path.dataset
dependencies = path.dependencies
# curr_dir = path.curr_dir"
curr_dir = "/Users/bene/Desktop/dataset2/captured/04_05_2021 10_24_58"

website_list = []

website_txt = "/Users/bene/Desktop/dataset2/websites.txt"

with open(website_txt) as file:
    content = file.read()
    websites = re.findall(r'(https?://[^\s]+)', content)
    # create folder with stripped url as name

for website in websites:
    website_list.append(website)


with open(os.path.join(dependencies, 'config.yml')) as f:
    config = yaml.safe_load(f)
    num = config["num"]


def call_websites():
    # for website in website_list:
    #     start_containers_1()
    driver1 = webdriver.Remote('http://127.0.0.1:4444')

    driver1.get("https://create-dataset.com")
    time.sleep(num)

    # stripped = website.replace("https://", "")
    # shutil.move(os.path.join(dataset, "sslkeylogfile_2.txt"),
    #             os.path.join(curr_dir, stripped))
    # shutil.move(os.path.join(dataset, "tcpdump_2.pcap"),
    #             os.path.join(curr_dir, stripped))

    # driver1.delete_all_cookies()
    # driver1.close()
    # driver1.quit()

    # stop_containers_1()


call_websites()
