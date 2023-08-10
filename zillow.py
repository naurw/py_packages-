# Converting to more modular format 
## Removing draft once testing has been completed 
## Do be advised that Zillow has a bot detection program in place--use at your discretion

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
    
    # Single instance webpage handling (scroll down for dynamic)
    # def parse_html(self):
    #     soup = BeautifulSoup(self.driver.page_source, 'html.parser')
    #     listings = soup.select('[class$="property-card-data"]')

    #     listing_links = [listing.find('a')['href'] for listing in listings]
    #     self.data['Href'] = listing_links

    #     listing_address = [listing.find('address').text for listing in listings]
    #     self.data['Address'] = listing_address

    #     listing_price = [listing.find('span', {'data-test': 'property-card-price'}).text[:-3] for listing in listings]
    #     self.data['Price'] = listing_price

    #     info_whole = [listing.find('ul', {'class': 'StyledPropertyCardHomeDetailsList-c11n-8-89-0__sc-1xvdaej-0 GlipV'}) for listing in listings]
    #     info_text = [[li.text for li in ul.find_all('li')] for ul in info_whole]
    #     self.data['Info'] = info_text


    # Modifying parse_html() to accomodate dynamic webpage following the limit set by scroll_down() 
    def parse_html(self):
        self.data = pd.DataFrame(columns=['Href', 'Address', 'Price', 'Info'])  # initializing the dataframe with column names

        while True:
            # Initialize a new soup object each time after scrolling
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            listings = soup.select('[class$="property-card-data"]')

            for listing in listings:
                href = listing.find('a')['href']
                address = listing.find('address').text
                price = listing.find('span', {'data-test': 'property-card-price'}).text[:-3]
                info_whole = listing.find('ul', {'class': 'StyledPropertyCardHomeDetailsList-c11n-8-89-0__sc-1xvdaej-0 GlipV'})
                info = [li.text for li in info_whole.find_all('li')]

                # Check if href already exists in our data
                if not any(self.data['Href'] == href):
                    new_row = {'Href': href, 'Address': address, 'Price': price, 'Info': info}
                    self.data = self.data.append(new_row, ignore_index=True)

            scrolled = self.scroll_down()

            if not scrolled:
                break  # If scroll_down returns False, we have reached the end of the page and exit the loop

    def scroll_down(self, limit = 5): 
        last_height = self.driver.execute_script('return document.body.scrollHeight') # get scroll height
        scroll_counter = 0 # initialize counter at 0 

        while True: 
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll down to the bottom

            sleep(5) # wait for pages to load

            new_height = self.driver.execute_script("return document.body.scrollHeight") # calculate new scroll height and compare with last scroll 
            if new_height == last_height or scroll_counter >= limit: # stop when it reaches the end or a hard stop at 5
                break
            last_height = new_height
            scroll_counter += 1  # Increment scroll counter 


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




