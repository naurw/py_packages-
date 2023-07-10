# Converting to more modular format 
## Removing draft once testing has been completed 
## Do be advised that Zillow has a bot detection program in place, hence this will only return the first few results--use at your discretion

import os
import pandas as pd
from time import sleep 
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime 
from datalogger.DataExport import DataExport
import os 

os.getcwd()


class Scraper:
    def __init__(self, config):
        self.config = config
        self.driver = self.init_driver()
        self.data = pd.DataFrame()
        self.date = datetime.now().strftime("%m%d%y")

    def init_driver(self):
        s = Service(self.config['CHROME_DRIVER_PATH'])
        options = webdriver.ChromeOptions()
        options.binary_location = self.config['BRAVE_PATH']
        options.add_argument(f"--user-agent={self.config['HEADER']['User-Agent']}")
        options.add_argument(f"--accept-language={self.config['HEADER']['Accept-Language']}")
        return webdriver.Chrome(service=s, options=options)

    def prompt_user_for_zipcode(self):
        self.driver.get(self.config['START'])

        if self.config['ZIP_CODE']:
            answer = input(f'The current zipcode is set to {self.config["ZIP_CODE"]}.\nDo you want to continue? (Y/N) ').strip().lower()
            if answer != 'y':
                self.config['ZIP_CODE'] = input('What zipcode would you like to search for? ').strip()
        else:
            self.config['ZIP_CODE'] = input('No zipcode currently set.\nWhat zipcode would you like to search for? ')

    def load_url(self):
        URL = f'{self.config["URL"]}/{self.config["ZIP_CODE"]}/'
        self.driver.get(URL)
        WebDriverWait(self.driver, 120).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))

    def parse_html(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        listings = soup.select('[class$="property-card-data"]')

        listing_links = [listing.find('a')['href'] for listing in listings]
        self.data['Href'] = listing_links

        listing_address = [listing.find('address').text for listing in listings]
        self.data['Address'] = listing_address

        listing_price = [listing.find('span', {'data-test': 'property-card-price'}).text[:-3] for listing in listings]
        self.data['Price'] = listing_price

        info_whole = [listing.find('ul', {'class': 'StyledPropertyCardHomeDetailsList-c11n-8-89-0__sc-1xvdaej-0 GlipV'}) for listing in listings]
        info_text = [[li.text for li in ul.find_all('li')] for ul in info_whole]
        self.data['Info'] = info_text

    def log_data(self):
        print(self.data.head(5))
        sleep(5)
        logger = DataExport(self.data, file_name=f'housing_data_{self.date}.xlsx', directory='my_logs')

    def reset_zipcode(self): 
        self.config['ZIP_CODE'] = None 

    def run(self):
        self.prompt_user_for_zipcode()
        self.load_url()
        self.parse_html()
        self.log_data()
        self.reset_zipcode()
        self.driver.quit()  

def main():
    config = {
        'CHROME_DRIVER_PATH': '/Users/William/Desktop/dev/chromedriver',
        'BRAVE_PATH': '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
        'HEADER': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        },
        'ZIP_CODE': None,
        'START': 'https://www.google.com/',
        'URL': 'https://www.zillow.com/homes/for_rent/'
    }

    scraper = Scraper(config)
    scraper.run()

if __name__ == "__main__":
    main()




