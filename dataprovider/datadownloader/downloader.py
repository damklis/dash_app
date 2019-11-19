from datadownloader.connection_decorator import connection_checker
import pandas as pd
import numpy as np
import thrift
import sasl
from pyhive import hive
from pyparsing import ParseException

class DataDownloader(object):

        def __init__(self, **kwargs):
            self.host = kwargs.get("host")
            self.user = kwargs.get("user")
            self.db = kwargs.get("database")
            self.__password = kwargs.get("password")
            self.__conn = self.make_hive_connection()
            self.category_type_col = [
                "baord_id", "levels_bundle",
                "app_version", "event_name"
            ]

        def connection_status(self):
            """
            Returns bool with information about connection status.
            """
            return self.__conn

        def make_hive_connection(self):
            """
            Setting up connection with Hive trough pyhive library.
            """
            try:
                self.__conn = hive.connect(
                    self.host,
                    username=self.user,
                    database=self.db
                )
                print("Connection with database succesfull.")
                return self.__conn
            except Exception as e:
                print("Problem with connection. More information: \n {}".format(e))
                return None

        @connection_checker
        def read_sql(self, sql_query):
            """
            Returns sql query output as pandas Dataframe. 
            """
            try:
                return pd.read_sql_query(sql_query, con=self.__conn)
            except ParseException as e:
                print("Chceck your query syntax. More info: {}".format(e))

        @staticmethod
        def change_to_category_type(df, category_columns):
            """
            Returns pandas Dataframe with optimized columns type.
            """
            for col in category_columns:
                if col in df.columns:
                    df[col] = df[col].astype("category")
                    return df
                else:
                    print("No board_id in columns. Returnning old DataFrame.")
                    return df

        @connection_checker
        def download_raw_events(self, sql_query, path):
            """
            Saves pandas Dataframe as pickle file into provided path.
            """
            print("Downloading raw events into {}.".format(path))
            dataframe = self.read_sql(sql_query)
            optimized_df = self.change_to_category_type(
                dataframe, self.category_type_col
                )
            print("Saving DataFrame as .pkl file.")
            optimized_df.to_pickle(path)

        def end_connection(self):
            """
            Closes connection with Hive.
            """
            print("Closing connection with the database.")
            self.__conn.close()
