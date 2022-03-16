from modules.scraper import Scraper


def main():
    #link = 'https://www.willhaben.at/iad/immobilien/immobilien/vorarlberg?rows=100'
    link = 'https://www.willhaben.at/iad/immobilien/eigentumswohnung/eigentumswohnung-angebote?sfId=30fdd1af-4da1-4099-a7d9-dd2f309dd6a7&isNavigation=true&page=1&rows=100'
    Scrape = Scraper(link, 'flat_buy', headless=True)
    Scrape.DbConn.drop_table()
    Scrape.DbConn.create_table()
    Scrape.scrape_link()

main()