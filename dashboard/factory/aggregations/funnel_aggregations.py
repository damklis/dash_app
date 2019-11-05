
import pandas as pd
import numpy as np
from factory.aggregations.base_aggregations import BaseAggregator


class FunnelAggregator(BaseAggregator):

    def __init__(self, dataframe, app_version):
        super().__init__(dataframe, app_version)
        self.max_steps = 25

    def add_board_id(self, df):
        '''
        This function filter DataFrame by version of application.
        '''
        if df['event_name'] == 'pet_type':
            return '010001'
        elif  df['event_name'] == 'chest':
            return '010106'
        else:
            return  df['board_id']
    
    def add_step_id(self, df):
        '''
        This function filter DataFrame by version of application.
        '''
        if df['event_name'] == 'start_game':
            return '0'
        elif df['event_name'] == 'end_game':
            return '7'
        elif df['event_name'] == 'chest':
            return '0'
        elif df['event_name'] == 'pet_type':
            return '1'
        else:
            return df['step']

    def add_step(self, row1, row2, row3):
        '''
        This function filter DataFrame by version of application.
        '''
        if row1 in ('pet_type', 'chest'):
            return row1
        elif row1 == 'tutorial_step':
            return row1[:8] + '_' + row2[4:] + '_' + row3
        else:
            return row1 + row2

    def create_funnel_df(self):
        '''
        Creating funnel table. This table will be used in chart as input data.
        '''
        # filtering DataFrame
        filtered_df = self.choose_appversion()

        # replacing NULLs with board_id and step_id values
        filtered_df['board_id'] = filtered_df.apply(self.add_board_id, axis=1)
        filtered_df['step_id'] = filtered_df.apply(self.add_step_id, axis=1)

        # grouping DataFrame
        df_pv = filtered_df.groupby(
            by=['event_name','board_id', 'step_id']
            ).agg({"total_users": np.sum}).fillna(0).reset_index()

        # calculating metrics
        df_pv['unique_users_%'] = df_pv['total_users'] / df_pv['total_users'].max() * 100
        df_pv['unique_users_%'] = df_pv['unique_users_%'].apply(lambda x: round(x,2))
        df_pv['step'] = df_pv.apply(lambda row: self.add_step(
            row['event_name'], row['board_id'], row['step_id']), axis=1)

        df_pv = df_pv[df_pv['step'] != 'tutorial_04_3/2']

        return df_pv.sort_values(by=['board_id', 'step_id'])[:self.max_steps]