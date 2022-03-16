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

# create browser and launch website

def initialize_driver(headless:bool=True) -> object:
    s = Service(ChromeDriverManager().install())
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=s, options=options)
    return driver

def deny_dataprivacy_notice(driver:object) -> None:
    try:
        privacy_deny = driver.find_element('xpath','//*[@id="didomi-notice-disagree-button"]')
        privacy_deny.click()
    except exceptions.NoSuchElementException:
        pass
    time.sleep(1) #avoid early scroll start
    return None


# scroll slowly through page
def scroll_page(driver:object, speed:int=400) -> None:
    page_height = driver.execute_script("return document.documentElement.scrollHeight")
    current_height = 0
    while current_height < page_height:
        current_height += speed
        driver.execute_script("window.scrollTo(0," + str(current_height) + ")")
    return None


def find_elements(driver:object) -> list:
    elements = driver.find_elements('css selector','.Box-sc-wfmb7k-0.ResultListAdRowLayout___StyledBox-sc-1rmys2w-0.ginNzk.dZyCtF')
    return elements


def next_page(driver:object, pattern:re.Pattern) -> bool:
    next_page = driver.find_element('xpath','//*[@id="skip-to-content"]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/nav/ul/li[6]')
    next_page_html = next_page.get_attribute('innerHTML')
    next_page.click()
    
    if len(re.findall(pattern, str(next_page_html))) == 0: #check if button is possible to click
        return False
    else:
        return True

def extract_info(element:bs.BeautifulSoup, pattern:re.Pattern) -> tuple:
    db_entry = {'title':'element.h3.text','location':'element.find("div", class_="Box-sc-wfmb7k-0 khvLsE").text' ,'footage':'element.find("div", class_="Text-sc-10o2fdq-0 iLQwFF").text', 'rooms':'re.search(pattern, str(element)).group(0)', 'features':'element.find("div", class_ = "Text-sc-10o2fdq-0 brNqZP").text', 'price':'element.find("span", class_ ="Text-sc-10o2fdq-0 eRKVmh").text', 'seller':'element.find("span", class_ = "Text-sc-10o2fdq-0 flpYRE").text', 'url': '"https://www.willhaben.at/"+element.a.get("href")'}
    for key, value in db_entry.items():
        try:
            db_entry[key] = eval(value)
        except AttributeError:
            db_entry[key] = None
    return db_entry


def scrape_link(link:str, headless:bool=True) -> None:
    
    driver = initialize_driver(headless)
    driver.get(link)
    deny_dataprivacy_notice(driver)


    next_page_available = True
    pattern_room = re.compile(r'\d(?=<\/span><span class=\"Text-sc-10o2fdq-0 iyzLep\"> <!-- -->Zimmer)')
    pattern_href = re.compile(r'href="')
    pages = 0
    start = datetime.now()
    while next_page_available:
        pages += 1
        scroll_page(driver)
        elements = find_elements(driver)

        # iterate through elements to extract data
        for elem in elements:
            elem_html = elem.get_attribute('innerHTML')
            elem_soup = bs.BeautifulSoup(elem_html, 'html.parser')
            db_entry = extract_info(elem_soup, pattern_room) # safe entry to database --> next step

        print(len(elements))

        next_page_available = next_page(driver, pattern_href)
    
    print('SCRAPING FINISHED')
    print(f'Pages: {pages}')
    print(f'It took {datetime.now()-start}')



def main():
    link = 'https://www.willhaben.at/iad/immobilien/immobilien/vorarlberg?rows=100'
    scrape_link(link, headless=True)

main()


