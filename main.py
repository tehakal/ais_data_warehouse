from modules.db_connector import db_connector
from modules.scraper import *


def main():
    link = 'https://www.willhaben.at/iad/immobilien/immobilien/vorarlberg?rows=100'
    scrape_link(link, headless=False)

main()