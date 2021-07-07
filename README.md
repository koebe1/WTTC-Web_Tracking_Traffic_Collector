# WTTC - WEB TRACKING TRAFFIC COLLECTOR

    Web Tracking Traffic Collector is an application that
    lets you collect web traffic of websites and
    label web tracking packets according to a filterlist.

    To do so it uses a web crawler in advance to the
    traffic collecting that generates a protocol of
    the used web trackers on the specified websites.
    On that basis the resulting dataset
    can be labeled as tracking and non tracking packets.

    Note that WTTC was written for the use on MAC OS.
    For the use on other operating systems changes have to be made to the source code.

    ###Built utilizing:

        * [uBlock Origin](https://ublockorigin.com/)
        * [Docker](https://www.docker.com/)
        * [Tcpdump](https://www.tcpdump.org/)
        * [Tshark](https://www.wireshark.org/docs/man-pages/tshark.html)

# Setup

    1. Check Chrome Version

        The Chromedriver used works for Mac OS Chrome Version 91.0.4472.114.
        For newer/older Version of Chrome get the according for your OS Chromedriver at
        -> https://chromedriver.chromium.org/ and copy it to the "dependencies" folder of the application.

    2. Add your Chrome Profile to dependencies/config.yml

        -> Windows 7, 8.1, and 10: C:\Users\<username>\AppData\Local\Google\Chrome\User
        Data\Default

        -> Mac OS X: Users/<username>/Library/Application Support/Google/Chrome/Default

        -> Linux: /home/<username>/.config/google-chrome/default

    3. Install uBlock Origin for Google Chrome

        To specify a filterlist of your choice go to
        -> chrome-extension://cjpalhdlnbpafiamejdnhcphjbkeiagm/dashboard.html#3p-filters.html and specify the web tracking filterlist of your choice.

    4. Get the Application

        Download the application from https://github.com/koebe1/web_traffic_collector or get it via your Terminal:
        -> git clone https://github.com/koebe1/web_traffic_collector.git
    5. Get Tshark at:

       -> https://tshark.dev/setup/install/

    6. Get Docker Desktop

        Download Docker Desktop at:
        -> https://www.docker.com/products/docker-desktop

    7. Add Your Path to Docker to dependencies/config.yml

    8. Get the Images for Docker

        Via Terminal:
        -> docker pull retreatguru/headless-chromedriver
        -> docker pull kaazing/tcpdump

    9. Install Python Dependencies

        Install from dependencies/requirements.txt via pip e.g.:
        -> pip install -r requirements.txt

    10. If your not on a Mac OS Change run_app to a Executable for your OS

# Settings

    The config.yml file gives you the ability to specify parameters of the application:

    1. "num" specifys the number of seconds to capture the uBlock protocol and the web traffic.

    2. "max_website_num" specifys the maximal websites that are opened at once when extracting the uBlock protocol.

    3. "timeout" sets a timeout in case a website doesen't finish loading correctly.

    4. "max_container_num" specifys max amount of containers that capture traffic at once.

    5. "chrome_profile" let's you specify your chrome profile to start chrome with.

    6. "docker_path" specifys the path to your docker location to start docker if it is not running already.

    7. "docker_startup_time" specifys time to wait for docker to start up before running the application if docker wasn't running already.

# Usage

    1. Specify the websites to call in websites.txt in the format "https://example.org".

    2. Run the executable file run_app to start the application.

    3. Choose a foldername to save your capture in.

    4. After the programm finishes running the output will be:

        -> a folder with the name you specified at captured/"yourFolderName"

            in that folder:

            -> "ublock_log.txt" the uBlock protocol

            -> "total_statistics.txt" a statistics file with the number of tracker in the ublock protocol
            and the captured data

            -> a folder for each website that was called

                in that folder:

                -> "blocked_urls_applicationsl.txt" a summary of the tracker urls from the captured data

                -> "sskeylogfile.txt" the ssl keylog file to decrypt the web traffic of the website

                -> "tcpdump.pcap" a pcap file with the captured data

                -> "data.json" a JSON file with the labeled data
