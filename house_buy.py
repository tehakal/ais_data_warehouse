from modules.scraper import Scraper


def main():
    link = 'https://www.willhaben.at/iad/immobilien/haus-kaufen/haus-angebote?sfId=4cf7211e-b774-421d-8bc4-39c2d9f1ab61&isNavigation=true&page=1&rows=100'
    next_link = '/html/body/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/nav/ul/li[last()]'  # seperate next links are necessary for different links
    
    Scrape = Scraper(link, 'house_buy', next_link=next_link, headless=True)
    Scrape.DbConn.create_table()
    Scrape.scrape_link()

main()