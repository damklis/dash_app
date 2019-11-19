import pandas as pd
import numpy as np

class BaseAggregator(object):

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def choose_appversion(self, app_version):
        """
        This function filter DataFrame by the version of the application.
        """
        return self.dataframe[self.dataframe["app_version"] == str(app_version)]\
            .drop_duplicates()

    def add_difficulty_level(self, column):
        """
        Returns column with mapped difficulty values. 
        """
        if column[2:4] == "01":
            return "normal"
        elif column[2:4] == "02":
            return "challenging"
        else:
            return "expert"

    def __str___(self):
        return f"BaseAggregator({self.dataframe.info()})"