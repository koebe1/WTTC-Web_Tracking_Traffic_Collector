import os.path
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import argparse
import re
import pyperclip
import yaml
import paths

dataset = paths.dataset


def extract_ublock_log(curr_dir):
    print("")
    print("Extracting uBlock log...")

    dependencies = paths.dependencies
    config = paths.config

    website_txt = f"{dataset}/websites.txt"

    # load data from config
    with open(config) as f:
        config = yaml.safe_load(f)
        num = config["num"]
        chrome_profile = config["chrome_profile"]

    # start chrome with uBlock and your user settings -> important for the filter list settings in uBlock
    options = webdriver.ChromeOptions()
    options.add_extension(
        os.path.join(dependencies, 'uBlock.crx'))

    options.add_argument(
        chrome_profile)

    browser = os.path.join(dependencies, 'chromedriver')
    driver = webdriver.Chrome(executable_path=browser, options=options)

    # specify the argument to call the python skript with --> -f "path to file"
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-f', help='specify a file with a list of urls')
    # args = parser.parse_args()

    # open file with websites, extract urls and push them to array "websites"
    with open(website_txt) as file:
        text = file.read()
        websites = re.findall(r'(https?://[^\s]+)', text)

    # calls websites and opens uBlock network protocoll

    def callWebsites():
        # opens uBlock extension
        driver.get(
            'chrome-extension://cjpalhdlnbpafiamejdnhcphjbkeiagm/logger-ui.html?popup=1')
        uBlock_window = driver.current_window_handle

        with open(os.path.join(dependencies, 'config.yml')) as f:
            config = yaml.safe_load(f)
            max_website_num = config["max_website_num"]

        tabs = []
        i = 0
        # open all websites in the websites.txt  (upper limit at once -> max_website_num)
        while i < len(websites):
            j = 0

            # open as many websites as max_website_num
            while max_website_num > j:
                if i < len(websites):
                    tab = websites[i].replace("https://", "").replace(".", "")
                    tabs.append(tab)
                    driver.execute_script(
                        f'''{tab}= window.open("{websites[i]}", "_blank");''')
                i += 1
                j += 1

            # wait "num" (config.yml) seconds
            time.sleep(num)

            # close open tabs
            for tab in tabs:
                driver.execute_script(
                    f'''{tab}.close();''')

        # switch to uBlock protocol
        for window_handle in driver.window_handles:
            if window_handle != uBlock_window:
                driver.switch_to.window(uBlock_window)
                break

    def extractBlockedContend():
        action = ActionChains(driver)

        filter_button = driver.find_element(
            By.ID, 'filterButton')

        blocked_button = driver.find_element(
            By.XPATH, '//*[@id="filterExprPicker"]/div[1]/span[2]')

        # move mouse over "filter_button" and click "blocked"
        action.move_to_element(filter_button).perform()
        blocked_button.click()

        time.sleep(0.5)

        # use JS because pythons click() method is not working to click the loggerExport Button
        a = "document.getElementById('loggerExport').click();"
        # select "Rohtext"
        c = """ let mainDiv = document.getElementById('loggerExportDialog');
                let childDiv = mainDiv.getElementsByTagName('div')[0];
                let childChildDiv = childDiv.getElementsByTagName('div')[1];
                let rohtext = childChildDiv.getElementsByTagName('span')[0];
                rohtext.click();
                """
        d = """
                let mainDiv = document.getElementById('loggerExportDialog');
                let childDiv = mainDiv.getElementsByTagName('div')[0];
                let childChildDiv = childDiv.getElementsByTagName('div')[2];
                let zwischenablage = childChildDiv.getElementsByTagName('span')[0];
                zwischenablage.click();
            """
        # execute the defined JS code a,c,d
        driver.execute_script(a)
        time.sleep(0.2)
        driver.execute_script(c)
        time.sleep(0.2)
        driver.execute_script(d)
        time.sleep(0.2)

        driver.quit()

    def writeClipboardToFile():

        joined_path = os.path.join(curr_dir, "ublock_log.txt")

        ublock_output = pyperclip.paste()
        f = open(joined_path, "w+")
        f.write(ublock_output)

    callWebsites()
    extractBlockedContend()
    writeClipboardToFile()
