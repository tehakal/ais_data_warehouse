from modules.scraper import Scraper


def main():
    #link = 'https://www.willhaben.at/iad/immobilien/immobilien/vorarlberg?rows=100'
    link = 'https://www.willhaben.at/iad/immobilien/d/haus-kaufen/oberoesterreich/linz/zum-verkaufen-552755797'
    Scrape = Scraper(link, 'house_buy', headless=True)
    Scrape.DbConn.drop_table()
    Scrape.DbConn.create_table()
    Scrape.scrape_link()

main()