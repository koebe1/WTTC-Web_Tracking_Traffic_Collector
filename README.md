# web traffic collector

Vorläufige Liste ReadMe:

- Docker Desktop notwendig

- Chromeversion & Chromedriver müssen zusammenpassen

- websites.txt nimmt nur websites mit Format https://example.com

- Python dependencies file --> pip install -r requirements.txt

---> (test with vm)

# SETUP

1. Check Chrome Version

   The Chromedriver used works for Chrome Version 91.0.4472.114.
   For newer/older Version of Chrome get the according Chromedriver at
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

5. Get Docker Desktop

   Download Docker Desktop at:
   -> https://www.docker.com/products/docker-desktop

6. Add Your Path to Docker to dependencies/config.yml

7. Get the Images for Docker

   Via Terminal:
   -> docker pull retreatguru/headless-chromedriver
   -> docker pull kaazing/tcpdump
