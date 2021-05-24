import os
import time
from selenium import webdriver
import multiprocessing.process


# docker run --rm -it --name chrome11 -p 4444:4444 -v "/Users/bene/Desktop/dataset/ssl":/ssl -e SSLKEYLOGFILE=ssl/sslkeylogfile.txt retreatguru/headless-chromedriver chromedriver --port=4444

websites = ['https://create-dataset.com',
            'https://bmw.de', 'https://apple.com', 'https://google.com', 'https://web.de', 'https://bild.de']


def call_website(website, port):
    driver = webdriver.Remote(f"http://127.0.0.1:{port}")
    driver.get(website)
    time.sleep(5)
    driver.quit()
    # print(f"Website {website} called on port {port}!")


def start_containers(website_num):

    max_container_num = 10
    port_num = 4444
    ports = []
    websites_num = len(websites)
    i = 0

    # number of containers is limited by number of cpus on the machine (for parallel website calls -> 1 call per cpu) or number of websites if that is smaller
    while max_container_num > i and i < websites_num:
        os.system(
            f'docker run --rm -d -it --name chrome{i} -p {port_num}:{port_num} --expose={port_num} -v "/Users/bene/Desktop/dataset2":/ssl -e SSLKEYLOGFILE=ssl/sslkeylogfile{i}.txt retreatguru/headless-chromedriver chromedriver --port={port_num} --whitelisted-ips=')
        os.system(
            f'docker run --rm -d --name tcpdump{i} --net=container:chrome{i} -v /Users/bene/Desktop/dataset2/:/tcpdump kaazing/tcpdump  not host 127.0.0.1 and not host 172.17.0.1 -v -i any -w  tcpdump/tcpdump{i}.pcap')

        ports.append(port_num)
        port_num += 1
        i += 1

    # define list for processes
    processes = []
    print(i)

    # start as many processes (website calls) as there are containers (i) with different websites and ports
    for _ in range(i):
        p = multiprocessing.Process(target=call_website, args=[
            websites[0], ports[0]])
        p.start()
        processes.append(p)
        # remove first element of website list and port list as they have already been called
        print(f"Website {websites[0]} called on port {ports[0]}!")
        websites.pop(0)
        ports.pop(0)

    # join processes to continue script if all processes are finished
    for process in processes:
        process.join()

    os.system("docker kill $(docker ps -q)")


if __name__ == "__main__":
    start_containers(5)


# c1 = multiprocessing.Process(
#     target=start_chrome11)

# c2 = multiprocessing.Process(
#     target=start_chrome22)

# c3 = multiprocessing.Process(
#     target=start_chrome33)

# c4 = multiprocessing.Process(
#     target=stop_containers)

# if __name__ == "__main__":
#     c1.start()
#     c2.start()
#     c3.start()
#     c4.start()
#     c1.join()
#     c2.join()
#     c3.join()
#     c4.join()
