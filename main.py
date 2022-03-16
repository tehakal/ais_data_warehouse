from modules.scraper import Scraper


def main():
    link = 'https://www.willhaben.at/iad/immobilien/immobilien/vorarlberg?rows=100'
    Scrape = Scraper(link, 'test_house', headless=True)
    Scrape.DbConn.drop_table('test_house')
    Scrape.DbConn.create_table()
    Scrape.scrape_link()

main()