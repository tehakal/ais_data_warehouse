import imp
import psycopg2 as pg
from psycopg2.errors import DuplicateTable
from modules.Enumerators import Table
from sqlalchemy import create_engine
import sys
import pandas as pd

class DbConnector:
    '''
    Class which provides functions to insert data entries, create relevant table and drop tables.
    '''
    
    def __init__(self, table:str,dsn:str="host=localhost dbname=willhaben_prop user=postgres password=0000") -> None:
        self.dsn = dsn
        self.table = table

    def __exec_sql(self, sql_str:str, data_entry_vars:dict=None):
        try:
            '''Opens, commits and closes the connection to the database while executing sql statement'''
            with pg.connect(self.dsn) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql_str, vars=data_entry_vars)
        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DbConnector\nMethodname: __exec_sql")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")

    def insert_db(self, data_entry_vars:dict):
        sql_str = "INSERT INTO " + self.table + "(title, location, footage, rooms, features, price, seller, url) VALUES (%(title)s, %(location)s, %(footage)s, %(rooms)s, %(features)s, %(price)s, %(seller)s, %(url)s);"
        self.__exec_sql(sql_str, data_entry_vars)

    def create_table(self):
        sql_str = "CREATE TABLE " + self.table + "(id serial PRIMARY KEY, title varchar, location varchar, footage varchar, rooms int, features varchar, price varchar, seller varchar, url varchar);"
        try:
            self.__exec_sql(sql_str)
        except DuplicateTable:
            '''Safety measure to avoid overwriting table'''
            print('Table ' + self.table + ' already exists!')
            input('Press enter to continue.')
            sys.exit()

    def drop_table(self):
        sql_str = "DROP TABLE " + self.table + ";"
        self.__exec_sql(sql_str)
    

    
    def drop_tables_if_exist(self):
        try:
            sql_str = "DROP TABLE IF EXISTS FACT_real_estate;"
            self.__exec_sql(sql_str)
            sql_str = "DROP TABLE IF EXISTS DIM_Feature;"
            self.__exec_sql(sql_str)
            sql_str = "DROP TABLE IF EXISTS DIM_Seller;"
            self.__exec_sql(sql_str)
            sql_str = "DROP TABLE IF EXISTS DIM_Location;"
            self.__exec_sql(sql_str)
            sql_str = "DROP TABLE IF EXISTS Real_Estate_Final;"
            self.__exec_sql(sql_str)
        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DbConnector\nMethodname: drop_tables_if_exist")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")

    def create_tables_if_not_exist(self):
        try:
            sql_str = "CREATE TABLE IF NOT EXISTS DIM_Feature " \
                "(feature_id serial PRIMARY KEY, feature_name varchar);"
            self.__exec_sql(sql_str)
            
            sql_str = "CREATE TABLE IF NOT EXISTS DIM_Seller " \
                "(seller_id serial PRIMARY KEY, name varchar);"
            self.__exec_sql(sql_str)
            
            sql_str = "CREATE TABLE IF NOT EXISTS DIM_Location " \
                "(location_id serial PRIMARY KEY, postalcode varchar, city varchar, "\
                    "district varchar, street varchar);"
            self.__exec_sql(sql_str)
            
            sql_str = "CREATE TABLE IF NOT EXISTS FACT_Real_Estate " \
                "(real_estate_id serial PRIMARY KEY, seller_id integer, footage integer,"\
                    "feature_id integer, location_id integer, price double precision, "\
                        "housing_type varchar, real_estate_type varchar, rooms integer, url varchar);"
            self.__exec_sql(sql_str)

            sql_str = "CREATE TABLE IF NOT EXISTS Real_Estate_Final " \
                "(real_estate_id serial PRIMARY KEY, title varchar, price double precision, "\
                    "footage integer, rooms integer, features varchar, "\
                    "seller varchar, postalcode varchar, city varchar, "\
                    "district varchar, street varchar, housing_type varchar, "\
                    "real_estate_type varchar, url varchar);"
            self.__exec_sql(sql_str)

        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DbConnector\nMethodname: create_tables_if_not_exist")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")

    def select_data(self):
        try:
            sql_str = f"SELECT * FROM {self.table};"
            with pg.connect(self.dsn) as conn:
                return pd.read_sql_query(sql_str, con=conn)
            
        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DbConnector\nMethodname: select_data")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")

    def persist_data(self, table:Table, df:pd.DataFrame=None):
        try:
            engine = create_engine('postgresql://postgres:dat@localhost/willhaben_prop')
            if table.value == Table.DIM_FEATURE.value:
                df.to_sql(name="dim_feature", con=engine, if_exists="append", index=False)
            elif table.value == Table.DIM_LOCATION.value:
                df.to_sql(name="dim_location", con=engine, if_exists="append", index=False)
            elif table.value == Table.DIM_SELLER.value:
                df.to_sql(name="dim_seller", con=engine, if_exists="append", index=False)
            elif table.value == Table.REAL_ESTATE_FINAL.value:
                df.to_sql(name="real_estate_final", con=engine, if_exists="append", index=False)
            elif table.value == Table.FACT_REAL_ESTATE.value:
                sql_str = "INSERT INTO fact_real_estate(seller_id, footage, feature_id, "\
                                                        "location_id, price, housing_type, "\
                                                        "real_estate_type, rooms, url) "\
	                        "SELECT  ds.seller_id, re.footage, df.feature_id, "\
                                    "dl.location_id, re.price, re.housing_type, "\
                                    "re.real_estate_type, re.rooms, re.url "\
                            "FROM real_estate_final AS re "\
                            "INNER JOIN dim_feature AS df ON re.features = df.feature_name "\
                            "INNER JOIN dim_location AS dl ON re.postalcode = dl.postalcode AND "\
                                                            "re.city = dl.city AND "\
                                                            "re. district = dl.district AND "\
                                                            "re.street = dl.street "\
                            "INNER JOIN dim_seller AS ds ON re.seller = ds.name;"
                
                self.__exec_sql(sql_str=sql_str)

        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DbConnector\nMethodname: select_data")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")
    
    def delete_duplicated(self, table:Table):
        try:
            if table.value == Table.DIM_FEATURE.value:
                sql_str = "DELETE " \
                            "FROM dim_feature AS dfa "\
                            "USING dim_feature AS dfb "\
                            "WHERE dfa.feature_id < dfb.feature_id "\
                            "AND dfa.feature_name = dfb.feature_name;"
            if table.value == Table.DIM_LOCATION.value:
                sql_str = "DELETE "\
                            "FROM dim_location AS dla "\
                            "USING dim_location AS dlb "\
                            "WHERE dla.location_id < dlb.location_id "\
                              "AND dla.postalcode = dlb.postalcode "\
                              "AND dla.city = dlb.city "\
                              "AND dla.district = dlb.district "\
                              "AND dla.street = dlb.street;"
            if table.value == Table.DIM_SELLER.value:
                sql_str = "DELETE " \
                            "FROM dim_seller AS dsa "\
                            "USING dim_seller AS dsb "\
                            "WHERE dsa.seller_id < dsb.seller_id "\
                              "AND dsa.name = dsb.name;"

            self.__exec_sql(sql_str=sql_str)

        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DbConnector\nMethodname: delete_duplicated")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")
