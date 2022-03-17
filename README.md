# ais_data_warehouse
Project to scrape data from the website *willhaben.at* and analyse it with business intelligence tools.

Four different categories are scraped:
- Wohnung mieten
- Wohnung kaufen
- Hau mieten
- Haus kaufen

The data was scraped with the help of [Python](https://www.python.org/) and the packages [Selenium](https://selenium-python.readthedocs.io/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

As a database management system [Postgres](https://www.postgresql.org/) was used with the python package [Psycopg](https://www.psycopg.org/docs/) to alter the database.


## Data Scraping & Data Insertion
The file `modules/db_connector.py`provides a class with the necessary functions to create the table and insert the data. `modules/scraper.py`imports `modules/db_connector.py` and additionally implements functions to navigate through web pages and select the elements with the help of regex. The python files in the main directory (`flat_buy.py`, `flat_rent.py`, `house_buy.py`, `house_rent.py`) call the necessary functions and provide the information to scrape the relevant category.

In the folder `database` a backup for the database is stored as well as scripts to create the database.