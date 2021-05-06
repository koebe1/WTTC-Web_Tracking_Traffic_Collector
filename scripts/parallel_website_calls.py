import multiprocessing
import time
import os
import os.path
import shutil
import yaml
from selenium import webdriver
from path import dataset, dependencies
# manage PARALLEL CALLS


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
