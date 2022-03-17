from modules.scraper import Scraper


def main():
    link = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sfId=54f3604d-74e9-4512-aeb8-a15787d6361f&isNavigation=true&page=1&rows=100'
    next_xpath = '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/nav/ul/li[last()]'    # seperate next links are necessary for different links
    
    Scrape = Scraper(link, 'flat_rent', next_xpath=next_xpath ,headless=True)
    Scrape.DbConn.create_table()
    Scrape.scrape_link()

main()