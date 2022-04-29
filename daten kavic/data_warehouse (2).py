from xmlrpc.client import boolean
from modules.db_connector import DbConnector
from modules.Enumerators import HousingType, RealEstateType, Table
import pandas as pd


class DataWarehouse:
    
    def __init__(self, table:str, drop_dim_fact_tables:bool) -> None:
        try:
            self.db_connection = DbConnector(table=table, dsn="host=localhost dbname=willhaben_prop user=postgres password=dat")
            if drop_dim_fact_tables:
                self.db_connection.drop_tables_if_exist()
            self.db_connection.create_tables_if_not_exist()
        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DataWarehouse\nMethodname: __init__")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n")
            print("**********************************************")

    def persist_data(self, housing_type:HousingType, real_estate_type:RealEstateType) -> None:
        try:
            df:pd.DataFrame = self.db_connection.select_data()
            df = self.prepare_data(df=df, housing_type=housing_type, real_estate_type=real_estate_type)
            
            dim_feature:pd.DataFrame = pd.DataFrame(df["features"].unique(), columns=["feature_name"])
            self.db_connection.persist_data(df=dim_feature, table=Table.DIM_FEATURE)
            dim_location:pd.DataFrame = df[["postalcode", "city", "district", "street"]].drop_duplicates()
            self.db_connection.persist_data(df=dim_location, table=Table.DIM_LOCATION)
            dim_seller:pd.DateOffset = pd.DataFrame(df["seller"].unique(), columns=["name"])
            self.db_connection.persist_data(df=dim_seller, table=Table.DIM_SELLER)
            real_estate_final = df[["title", "price", "footage", "rooms", "features", "seller",
                                    "postalcode", "city", "district", "street", "housing_type",
                                    "real_estate_type", "url"]]
            self.db_connection.persist_data(df=real_estate_final, table=Table.REAL_ESTATE_FINAL)
            self.db_connection.persist_data(table=Table.FACT_REAL_ESTATE)
            self.db_connection.delete_duplicated(table=Table.DIM_FEATURE)
            self.db_connection.delete_duplicated(table=Table.DIM_LOCATION)
            self.db_connection.delete_duplicated(table=Table.DIM_SELLER)

        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DataWarehouse\nMethodname: persist_data")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")

    def prepare_data(self, df:pd.DataFrame, housing_type:HousingType, real_estate_type:RealEstateType) -> pd.DataFrame:
        try:
            df["real_estate_type"] = real_estate_type.value
            df["housing_type"] = housing_type.value
            df["features"] = df["features"].str.replace("<!-- -->", "")
            df["price"] = df["price"].str.replace("€ ", "")
            df["price"] = df["price"].str.replace(".", "")
            df["price"] = df["price"].str.replace(" ", "")
            df["price"] = df["price"].str.replace(",", ".")
            return self.split_location(df=df)
        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DataWarehouse\nMethodname: clear_data")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")

    def split_location(self, df:pd.DataFrame) -> pd.DataFrame:
        try:
            df["postalcode"] = None; df["city"] = None; df["district"] = None; df["street"] = None

            for index, location in enumerate(df['location']):
                location_parts = location.split(", ") 
                if location_parts is not None and len(location_parts) > 0:
                    postalcode_city = location_parts[0].split(" ", 1)
                    if len(postalcode_city) > 1:
                        df.loc[index, "postalcode"] = postalcode_city[0]
                        df.loc[index, "city"] = postalcode_city[1]
                    else:
                        df.loc[index, "city"] = postalcode_city[0]
                if (location_parts is not None and df.loc[index, "city"] == "Wien" 
                    and len(location_parts) > 2):
                    df.loc[index, "district"] = location_parts[1]
                    df.loc[index, "street"] = location_parts[2]
                elif location_parts is not None and len(location_parts) >= 2:
                    df.loc[index, "street"] = location_parts[1]   

            return df          
        except Exception as err:
            print("**********************************************") 
            print(f"Classname: DataWarehouse\nMethodname: split_location")
            print(f"\nFollowing exception occured: \nUnexpected {err}\nErrortype: {type(err)}\n") 
            print("**********************************************")
            

