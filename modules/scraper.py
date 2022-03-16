import bs4 as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import exceptions
import re as re
from datetime import datetime
import time
from .db_connector import DbConnector

# create browser and launch website

class Scraper():

    def __init__(self, link:str, table:str, headless:bool=True) -> None:
        self.__headless = headless
        self._pattern_room = re.compile(r'\d+(?=<\/span><span class=\"Text-sc-10o2fdq-0 iyzLep\"> (<!-- -->)?Zimmer)')
        self._pattern_footage = re.compile(r'\d+(?=<\/span><span class=\"Text-sc-10o2fdq-0 iyzLep\"> (<!-- -->)?m²)')
        self._pattern_features = re.compile(r'(?<=<span class=\"Text-sc-10o2fdq-0 iyzLep\"> )(?:<!-- -->|)[a-zA-Z/\u00fc\u00f6\u00e4\u00df\u00dc\u00d6\u00c4]*(?=<\/span>)')
        self.__pattern_href = re.compile(r'href="')

        self.__page_available = True
        self.DbConn = DbConnector(table)
        self.scraped_pages = 0
        self.link = link
        self.initialize_driver()



    def initialize_driver(self) -> object:
        s = Service(executable_path=ChromeDriverManager().install())
        options = Options()
        if self.__headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(service=s, options=options)


    def deny_dataprivacy_notice(self) -> None:
        try:
            privacy_deny = self.driver.find_element('xpath','//*[@id="didomi-notice-disagree-button"]')
            privacy_deny.click()
        except exceptions.NoSuchElementException:
            pass
        time.sleep(1) #avoid early scroll start
        return None


    # scroll slowly through page
    def scroll_page(self, speed:int=400) -> None:
        page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        current_height = 0
        while current_height < page_height:
            current_height += speed
            self.driver.execute_script("window.scrollTo(0," + str(current_height) + ")")


    def find_elements(self) -> list:
        self.elements = self.driver.find_elements('css selector','.Box-sc-wfmb7k-0.ResultListAdRowLayout___StyledBox-sc-1rmys2w-0.ginNzk.dZyCtF')


    def next_page(self) -> bool:
        next_page = self.driver.find_element('xpath','//*[@id="skip-to-content"]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/nav/ul/li[6]')
        next_page_html = next_page.get_attribute('innerHTML')
        next_page.click()
        
        if len(re.findall(self.__pattern_href, str(next_page_html))) == 0: #check if button is possible to click
            self.__page_available = False
        else:
            self.__page_available = True

    def __extract_info(self, element:bs.BeautifulSoup) -> tuple:
        db_entry = {'title':'element.h3.text','location':'element.find("div", class_="Box-sc-wfmb7k-0 khvLsE").text' ,'footage':'re.search(self._pattern_footage, str(element)).group(0)', 'rooms':'re.search(self._pattern_room, str(element)).group(0)', 'features':'re.findall(self._pattern_features, str(element))', 'price':'element.find("span", class_ ="Text-sc-10o2fdq-0 eRKVmh").text', 'seller':'element.find("span", class_ = "Text-sc-10o2fdq-0 flpYRE").text', 'url': '"https://www.willhaben.at/"+element.a.get("href")'}
        for key, value in db_entry.items():
            try:
                db_entry[key] = eval(value)
            except AttributeError:
                db_entry[key] = None

        '''
        Since features do not have a unique pattern to match for, it has to be made sure that the string 'Zimmer does not match'. Additionally the pattern is different depending on the amount of other attributes resulting in the checks below and the re.findall() function call above.
        '''
        len_features = len(db_entry['features'])
        if len_features == 2: 
            db_entry['features'] = db_entry['features'][1]
        elif (len_features == 1) and ('Zimmer' not in db_entry['features']):
            db_entry['features'] = db_entry['features'][0]
        else:
            db_entry['features'] = None

        return db_entry


    def scrape_link(self) -> None:
        
        self.driver.get(self.link)
        self.deny_dataprivacy_notice()

        # setup necessary parameters
        self.start_time = datetime.now()
        while self.__page_available:
            self.scraped_pages += 1
            self.scroll_page()
            self.find_elements()

            # iterate through elements to extract data
            for elem in self.elements:
                elem_html = elem.get_attribute('innerHTML')
                elem_soup = bs.BeautifulSoup(elem_html, 'html.parser')
                db_entry = self.__extract_info(elem_soup) # safe entry to database --> next step
                self.DbConn.insert_db(db_entry)

            print(f'PageNr.: {self.scraped_pages}')

            self.next_page()
        
        print('SCRAPING FINISHED')
        print(f'Pages: {self.scraped_pages}')
        print(f'It took {datetime.now()-self.start_time}')



