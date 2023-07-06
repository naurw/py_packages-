# Rough draft 

from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep 
import pandas as pd
import os
os.getcwd()
from datalogger.DataExport import DataExport

# Static constants 
CHROME_DRIVER_PATH = '/Users/William/Desktop/dev/chromedriver' 
BRAVE_PATH = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
ZIP_CODE = None
START = 'https://www.google.com/'
URL = 'https://www.zillow.com/homes/for_rent/'

# Setting webdriver with headers from dictionary as well as using Brave as our default
s = Service(CHROME_DRIVER_PATH)
options = webdriver.ChromeOptions()
options.binary_location = BRAVE_PATH 
options.add_argument(f"--user-agent={HEADER['User-Agent']}")
options.add_argument(f"--accept-language={HEADER['Accept-Language']}")
driver = webdriver.Chrome(service = s, options = options)

driver.get(START)

# Prompt user for zipcode and modify URL based on user response | Load webpage esp for websites that rely heavily on JavaScript
if ZIP_CODE is not None: 
    while True:
        answer = input(f'The current zipcode is set to {ZIP_CODE}.\nDo you want to continue? (Y/N) ').strip().lower()
        if answer in ['y', 'n']: 
            break 
        print("Error: Please enter 'Y' or 'N'")

    if answer != 'y': 
        while True: 
            ZIP_CODE = input('What zipcode would you like to search for? ').strip() 
            if ZIP_CODE and ZIP_CODE.isdigit() and len(ZIP_CODE) == 5: 
                break 
            print("Error: Please enter a valid 5-digit zipcode.")

elif ZIP_CODE is None: 
    ZIP_CODE = input(f'No zipcode currently set.\nWhat zipcode would you like to search for? ')


## Add while loop here to ensure specific user inputs 

URL = f'{URL}/{ZIP_CODE}/'
driver.get(URL)
WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))

# Find listings and extract data from target class 
soup = BeautifulSoup(driver.page_source, 'html.parser')
listings = soup.select('[class$="property-card-data"]') 
listings

# Retrieve the links nested within the listings; there is only one href / hyperlink per listing 
## Generate a dataframe using this 
listing_links = [listing.find('a')['href'] for listing in listings] 

df = pd.DataFrame(listing_links, columns = ['Href'])

listing_address = [listing.find('address').text for listing in listings]
df['Address'] = listing_address

listing_price = [listing.find('span', {'data-test': 'property-card-price'}).text[:-3] for listing in listings]
df['Price'] = listing_price

info_whole = [listing.find('ul', {'class': 'StyledPropertyCardHomeDetailsList-c11n-8-89-0__sc-1xvdaej-0 GlipV'}) for listing in listings]
info_text = [[li.text for li in ul.find_all('li')] for ul in info_whole] # nested list comp with a list of strings where each string is separated by the 'ul' tag 
df['Info'] = info_text

df

logger = DataExport(df, file_name = 'housing_data_070523', directory = 'my_logs')
###################################################################################################################
###################################################################################################################
# listing_links_2 = []
# for listing in listings: 
#     href = listing.find('a')['href']
#     listing_links_2.append(href)

# matching_elements = set(listing_links).intersection(listing_links_2)
# num_matches = len(matching_elements)
# print(f'listing_links: {len(listing_links)}\n\nlisting_links_2: {len(listing_links_2)}\n\nMatched: {num_matches}')
###################################################################################################################
###################################################################################################################




# Converting to more modular format 

import os
import pandas as pd
from time import sleep 
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
import datalogger 
from datalogger.DataExport import DataExport
import os 

os.getcwd()


class Scraper:
    def __init__(self, config):
        self.config = config
        self.driver = self.init_driver()
        self.data = pd.DataFrame()

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
        logger = DataExport(self.data, file_name='housing_data_070523', directory='my_logs')

    def run(self):
        self.prompt_user_for_zipcode()
        self.load_url()
        self.parse_html()
        self.log_data()

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



