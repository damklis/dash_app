import pandas as pd
import numpy as np
from factory.aggregations.base_aggregations import BaseAggregator
import math


class EconomyAgregator(BaseAggregator):

    def __init__(self, dataframe, app_version):
        super().__init__(dataframe, app_version)

    def create_economy_df(self, lvls_bundle):
        '''
        Creating economy table. This table will be used in chart as input data.
        '''
        # filtering DataFrame
        filtered_df = self.choose_appversion()
        lvls_df = filtered_df[filtered_df['levels_bundle'].isin(lvls_bundle)]

        if len(lvls_bundle) != 0:
            return lvls_df.sort_values(by='level')

        return filtered_df.sort_values(by='level')