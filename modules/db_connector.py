import psycopg2 as pg
from psycopg2.errors import DuplicateTable
import sys

class DbConnector:
    '''
    Class which provides functions to insert data entries, create relevant table and drop tables.
    '''
    
    def __init__(self, table:str,dsn:str="host=localhost dbname=willhaben_prop user=postgres password=0000") -> None:
        self.dsn = dsn
        self.table = table

    def __exec_sql(self, sql_str:str, data_entry_vars:dict=None) -> None:
        with pg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_str, vars=data_entry_vars)

    def insert_db(self, data_entry_vars:dict):
        sql_str = "INSERT INTO " + self.table + "(title, location, footage, rooms, features, price, seller, url) VALUES (%(title)s, %(location)s, %(footage)s, %(rooms)s, %(features)s, %(price)s, %(seller)s, %(url)s);"
        self.__exec_sql(sql_str, data_entry_vars)

    def create_table(self):
        sql_str = "CREATE TABLE " + self.table + "(id serial PRIMARY KEY, title varchar, location varchar, footage varchar, rooms int, features varchar, price varchar, seller varchar, url varchar);"
        try:
            self.__exec_sql(sql_str)
        except DuplicateTable:
            print('Table ' + self.table + ' already exists!')
            input('Press enter to continue.')
            sys.exit()

    def drop_table(self):
        sql_str = "DROP TABLE " + self.table + ";"
        self.__exec_sql(sql_str)

