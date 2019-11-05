import pandas as pd
import numpy as np

class BaseAggregator(object):

    def __init__(self, dataframe, app_version):
        self.dataframe = dataframe
        self.app_version = app_version

    def choose_appversion(self):
        '''
        This function filter DataFrame by version of application.
        '''
        return self.dataframe[self.dataframe['app_version'] == self.app_version]\
            .drop_duplicates()

    def add_difficulty_level(self, column):
        '''
        Adding column with difficulty level.
        '''
        if column[2:4] == '01':
            return 'normal'
        elif column[2:4] == '02':
            return 'challenging'
        else:
            return 'expert'

    def __str___(self):
        return "Test"