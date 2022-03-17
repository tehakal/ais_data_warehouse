from modules.scraper import Scraper


def main():
    #link = 'https://www.willhaben.at/iad/immobilien/immobilien/vorarlberg?rows=100'
    link = 'https://www.willhaben.at/iad/immobilien/haus-kaufen/haus-angebote?sfId=4cf7211e-b774-421d-8bc4-39c2d9f1ab61&isNavigation=true&page=1&rows=100'
    Scrape = Scraper(link, 'house_buy', next_link='/html/body/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/nav/ul/li[last()]', headless=True)
    Scrape.DbConn.drop_table()
    Scrape.DbConn.create_table()
    Scrape.scrape_link()

main()