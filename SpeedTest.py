# v4
#### ---- Version History ---- #### 
#  - v1: POP, initialized boiler code for OOP  
#  - v2: revised OOP 
#  - v3: added logging framework 
#  - v4: implemented and revised logging with creation of `DataLogger` package  
import os 
from datetime import datetime 
import pandas as pd 
from time import sleep, time 
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
import tkinter as tk 
from tkinter import messagebox

import sys 
sys.path.append('/Users/William/Desktop/py_packages-')
from DataLogger import DataLogger  

env_file = '/Users/William/Desktop/creds.env'
load_dotenv(find_dotenv(env_file))

class SpeedTest: 

    ACCOUNT_EMAIL = os.getenv('twitter_email')
    ACCOUNT_PASSWORD = os.getenv('twitter_pass')
    PROMISED_DOWNLOAD = 300 
    CHROME_DRIVER_PATH = '/Users/William/Desktop/dev/chromedriver'
    CURRENT_PATH = os.getcwd() 


    def __init__(self): 
        self.s = Service(self.CHROME_DRIVER_PATH)
        self.options = Options()
        self.options.add_experimental_option('detach', True)
        self.options.add_argument('--start-maximized')
        self.options.page_load_strategy = 'normal'
        self.options.headless = False 
        self.driver = webdriver.Chrome(service = self.s, options = self.options)
        self.log_date = None 
        self.log_time = None 
        self.log_file_path = None 
        self.max_retries = 3 
        self.df = pd.DataFrame(columns = ['Date', 'Time', 'Download', 'Upload'])
        self.main_window = None 
        self.gui = tk.Tk() 
        self.gui.withdraw() 

    def _run_speed_test(self): 
        loading_browser = time() 
        self.driver.get('http://www.speedtest.net')
        WebDriverWait(self.driver, 120).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))
        start_test = time()
        self.log_date = datetime.now().strftime("%Y/%m/%d")
        self.log_time = datetime.now().strftime("%H:%M:%S")
        print(f'#### Logs #### \n\n {self.log_date} | {self.log_time} | {round(start_test - loading_browser,2)}s\n')

        download, upload, isp_provider = self._get_speed_test_results(self.driver)
        end_test = time() 
        print(f'#### Speed Test Results #### Provider: {isp_provider} | Download: {download} Mbps | Upload: {upload} Mbps | Run Time: {round(end_test-start_test,2)}')
        self.df = self.df.append(
                {
                    'Date': self.log_date,
                    'Time': self.log_time,
                    'Download': download,
                    'Upload': upload
                }, ignore_index = True
            )
        
        print(self.CURRENT_PATH)

        logger = DataLogger(self.df)

        if download < self.PROMISED_DOWNLOAD - 50: 
            message = f'Received {download} Mbps even though I currently have the plan that promises {self.PROMISED_DOWNLOAD} Mbps.\n\nDo you want to complain on Twitter?'
            complain_answer = messagebox.askyesno(title = 'Confirmation', message = message)
            if complain_answer: 
                print('Starting complaint using credentials provided in dotenv file.')
                self._login_to_twitter(self.driver)
            else: 
                print('Data has been logged for reference.')
                self.driver.quit() 
            """messagebox.askyesorno() does not need messagebox.showinfo(). does require tk.Tk().mainloop() for event listening post conditional statements"""
            self.gui.mainloop() 

    def _retry_speed_test(self): 
        retry_counter = 0 
        while True: 
            try: 
                self._run_speed_test() 
                break 
            except Exception: 
                retry_counter += 1 
                if retry_counter >= self.max_retries: 
                    print(f'Failed to run speed test after {self.max_retries} attempts.')
                    break 
            print(f'Speed test failed. Retrying in 10 seconds... Attempt {retry_counter}/{self.max_retries}')
            sleep(10) 

    def _get_speed_test_results(self, driver): 
        go_button = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        go_button.click()
        sleep(60)
        isp_provider = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[4]/div/div/div[1]/div[3]/div[2]')
        download = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
        download = float(download.text)
        upload = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
        upload = float(upload.text)
        return download, upload, isp_provider

    def _login_to_twitter(self, driver): 
        try: 
            driver.get('http://www.twitter.com')
            WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))
            sleep(2)
            login = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div[1]/div/div/div/div/div/div/div/div[1]/a')
            login.click()
            sleep(2)
            driver.implicitly_wait(10)
            login_apple_id = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[3]')
            login_apple_id.click()
            print(driver.title)
            self.main_window = driver.current_window_handle
            apple_id_login_window = driver.window_handles[-1]
            driver.switch_to.window(apple_id_login_window)
            print(driver.title)
            input_apple_id = driver.find_element(By.XPATH, '//*[@id="account_name_text_field"]')
            for ele in self.ACCOUNT_EMAIL:
                input_apple_id.send_keys(ele)
                sleep(.1) 
            input_apple_id.send_keys(Keys.ENTER)
            input_apple_id_pass = driver.find_element(By.XPATH, '//*[@id="password_text_field"]')
            for ele in self.ACCOUNT_PASSWORD:
                input_apple_id_pass.send_keys(ele)
                sleep(.1) 
            input_apple_id_pass.send_keys(Keys.ENTER)

            self._apple_id_handler(self.driver) 
        except TimeoutException: 
            print('Timed out waiting for page--retrying')
            self.driver.quit() 
            self._run_speed_test(self.driver)

    def _apple_id_handler(self, driver):
        try: 
            print(driver.title)
            two_factor_authentication = driver.find_element(By.XPATH, '//*[@id="stepEl"]/hsa2/div/verify-device/div/div/div[1]/security-code') # <-- web element not scriptable == incorrectly indexed a non-list item
            if two_factor_authentication.is_displayed():
                print('\n\nManually verify before continuing to next step.\n\nDO NOT need to PRESS TRUST brwowser.\n\n')
                sleep(60)
                driver.implicitly_wait(10)
                trust_browser = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[3]/div/button[3]')
                trust_browser.click()
                sleep(5)
                continue_browser = driver.find_element(By.XPATH, '/html/body/div[1]/oauth-init/div[1]/div/oauth-profile/div/div/idms-step/div/div/div/div[3]/idms-toolbar/div/div/div/button[1]')
                continue_browser.click()
                print(driver.title)
                print('Passed Apple ID verification and proceeding to tweet')

        except (NoSuchElementException, ElementClickInterceptedException): 
            print('Unable to locate element, continue manuallly by pressing trust browser')
            sleep(30)
            
        else:
            print(driver.title)
            driver.switch_to.window(self.main_window)
            # print(driver.title)
            skip_for_now = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]')
            if skip_for_now.is_displayed(): 
                skip_for_now.click() 
            try: 
                tweet = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
                tweet.click()
                compose = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div/div/div/div/label/div[1]/div/div/div/div/div/div/div/div/div/div')
                download = self._get_speed_test_results(driver)
                download = download[0]
                text = f'Currently have Optimum 300 and yet my network download speeds are only {download} Mbps... Optimum please step it up already.'
                for ele in text: 
                    compose.send_keys(ele) 
                    sleep(.1)
            except StaleElementReferenceException: 
                print('Issue with driver.window_handles / check driver')
            except NoSuchElementException: 
                print('Unable to locate element--complete manually / XPATH(s) might have changed')

# SpeedTest()._run_speed_test() 


if __name__ == '__main__': 
    speedtest = SpeedTest()
    speedtest._run_speed_test()
    speedtest.driver.quit() 

## Optimization ideas 

# import os
# import sys
# import time
# import logging.config
# import tkinter as tk
# from pathlib import Path
# from configparser import ConfigParser
# from datetime import datetime
# from time import sleep
# from dotenv import load_dotenv, find_dotenv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import (
#     TimeoutException,
#     NoSuchElementException,
#     StaleElementReferenceException,
#     ElementClickInterceptedException,
# )
# from tkinter import messagebox
# from DataLogger import DataLogger


# class SpeedTest:
#     CONFIG_FILE = 'config.ini'
#     LOGGING_CONFIG = 'logging.ini'
#     LOGS_DIR = 'logs'
#     DATE_FORMAT = '%Y/%m/%d'
#     TIME_FORMAT = '%H:%M:%S'
#     RETRY_INTERVAL = 10
#     MAX_RETRIES = 3
#     PROMISED_DOWNLOAD = None
#     CHROME_DRIVER_PATH = None

#     def __init__(self):
#         self.load_config()
#         self.load_env()
#         self.init_logging()
#         self.init_driver()
#         self.init_dataframe()
#         self.init_gui()

#     def load_config(self):
#         parser = ConfigParser()
#         parser.read(self.CONFIG_FILE)
#         self.PROMISED_DOWNLOAD = int(parser['SpeedTest']['PROMISED_DOWNLOAD'])
#         self.CHROME_DRIVER_PATH = parser['SpeedTest']['CHROME_DRIVER_PATH']

#     def load_env(self):
#         env_file = find_dotenv()
#         if env_file:
#             load_dotenv(env_file)

#     def init_logging(self):
#         Path(self.LOGS_DIR).mkdir(exist_ok=True)
#         logging.config.fileConfig(self.LOGGING_CONFIG)

#     def init_driver(self):
#         service = Service(self.CHROME_DRIVER_PATH)
#         options = Options()
#         options.add_experimental_option('detach', True)
#         options.add_argument('--start-maximized')
#         options.page_load_strategy = 'normal'
#         options.headless = False
#         self.driver = webdriver.Chrome(service=service, options=options)

#     def init_dataframe(self):
#         self.df = pd.DataFrame(columns=['Date', 'Time', 'Download', 'Upload'])

#     def init_gui(self):
#         self.gui = tk.Tk()
#         self.gui.withdraw()

#     def run_speed_test(self):
#         start_time = time.time()
#         self.logger.info('Loading speedtest.net')
#         self.driver.get('http://www.speedtest.net')
#         WebDriverWait(self.driver, 120).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))
#         loading_time = time.time() - start_time
#         self.log_date = datetime.now().strftime(self.DATE_FORMAT)
