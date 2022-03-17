from modules.scraper import Scraper


def main():
    #link = 'https://www.willhaben.at/iad/immobilien/immobilien/vorarlberg?rows=100'
    link = 'https://www.willhaben.at/iad/immobilien/eigentumswohnung/eigentumswohnung-angebote?sfId=30fdd1af-4da1-4099-a7d9-dd2f309dd6a7&isNavigation=true&page=1&rows=100'
    Scrape = Scraper(link, 'flat_buy_v2', next_link='/html/body/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/nav/ul/li[last()]',headless=True)
    Scrape.DbConn.create_table()
    Scrape.scrape_link()

main()