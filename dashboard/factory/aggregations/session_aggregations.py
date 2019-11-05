import pandas as pd
import numpy as np
from factory.aggregations.base_aggregations import BaseAggregator

class SessionAgregator(BaseAggregator):

    def __init__(self, dataframe, app_version):
        super().__init__(dataframe, app_version)

    def create_session_stats(self):
        '''
        Creating session stats. This table will be used in chart as input data.
        '''
        # filtering DataFrame
        filtered_df = self.choose_appversion()
        
        glob_sess_mean = round(filtered_df['sess_time'].mean() / 60,2)
        glob_sess_median = round(filtered_df['sess_time'].median() / 60,2)

        # calculating metrics
        df_pvt = filtered_df.groupby('session').agg(
            lambda x: len(x.unique())
                ).reset_index()

        df_pvt['drop'] = round(df_pvt['user_id'] / df_pvt['user_id'].max() * 100, 2)

        df = df_pvt[['session', 'drop']]

        return (glob_sess_mean, glob_sess_median, df)