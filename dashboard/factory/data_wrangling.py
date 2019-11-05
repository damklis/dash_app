import pandas as pd
import numpy as np
import math


def get_n_last_versions(df: pd.DataFrame, n_value: int):
    '''
    Extracts last n global versions of application.
    '''
    list_of_versions = sorted(
        df["app_version"].unique().tolist(),
        reverse=True
    )
    
    return tuple(list_of_versions[:n_value])


def add_difficulty_level(column: pd.Series):
    '''
    Adding column with difficulty level.
    '''
    #column = str(column)
    if column[2:4] == '01':
        return 'normal'
    elif column[2:4] == '02':
        return 'challenging'
    else:
        return 'expert'

def add_randomness_label(column: pd.Series):
    '''
    Adding column with randomnes level.
    '''
    if 0 <= column <= 3:
        return 'low'
    elif 3 < column <= 7:
        return 'medium'
    else:
        return 'high'

def choose_appversion(df: pd.DataFrame, app_version: str):
    '''
    This function filter DataFrame by version of application.
    '''
    df = df[df['app_version'] == str(app_version)].drop_duplicates()
    return df

def calculate_std_err(df):
    num = df['win_ratio_%'] * (100 - df['win_ratio_%'])
    den = df['total_games']
    std_err = math.sqrt(num/den)
    return round(std_err, 2)




def win_ratio_table(df, app_version, lvls_bundle,
        diff_level=['normal', 'challenging', 'expert'],
        randomness_level=['low', 'medium', 'high']):
    '''
    Creating result table. This table will be used in chart as input data.
    '''
    # filtering DataFrame
    filtered_df = choose_appversion(df, app_version)
    lvls_df = filtered_df[filtered_df['levels_bundle'].isin(lvls_bundle)]

    def win_ratio_helper(df_help):
        df_pv = df_help.groupby('board_id').agg(
                {'total_games': np.sum,
                'wins': np.sum,
                'loss': np.sum,
                'moves_left':np.mean,
                'iqr': np.mean,
                'median_attempt': np.mean
                }
        ).reset_index()

        df_pv['loss'] = df_pv['loss'].fillna(0)
        df_pv['win_ratio_%'] = df_pv['wins'] / df_pv['total_games'] * 100
        df_pv['randomness'] = df_pv['iqr'].apply(add_randomness_label)
        df_pv['win_ratio_%'] = df_pv['win_ratio_%'].apply(lambda x: round(x,2))
        df_pv['diff_level'] = df_pv['board_id'].apply(add_difficulty_level)
        df_pv['moves_left'] = round(df_pv['moves_left'],2)
        df_pv['std_err_%'] = df_pv.apply(lambda x: calculate_std_err(x), axis=1)

        df_pv = df_pv[df_pv['diff_level'].isin(diff_level)]

        return df_pv[df_pv['randomness'].isin(randomness_level)]

    # returning filtered Dataframe or Default Dataframe
    if len(lvls_bundle) != 0:
        return win_ratio_helper(lvls_df)
    return win_ratio_helper(filtered_df)


def drop_rate_table(df, app_version, lvls_bundle,
        diff_level=['normal', 'challenging', 'expert']):
    # filtering DataFrame
    filtered_df = choose_appversion(df, app_version)
    lvls_df = filtered_df[filtered_df['levels_bundle'].isin(lvls_bundle)]

    def drop_rate_hepler(df):
        # grouping DataFrame
        df_pv = df.groupby(by='board_id').agg(
                    {"total_users": np.sum}).fillna(0).reset_index()

        # calculating metrics
        df_pv['diff_level'] = df_pv['board_id'].apply(add_difficulty_level)
        df_pv['stay_rate_%'] = round(df_pv['total_users'] / df_pv['total_users'].max(),4) *100
        df_pv['drop_rate_%'] = 100.00 - df_pv['stay_rate_%']
        df_pv['shift'] = df_pv['drop_rate_%'].shift(1).fillna(0)
        df_pv['diff_%'] = df_pv['drop_rate_%'] - df_pv['shift']
        df_pv['diff_%'] = df_pv['diff_%'].apply(lambda x: 0 if x < 0 else x)
        df_pv[['drop_rate_%', 'stay_rate_%', 'diff_%']] = df_pv[['drop_rate_%',
            'stay_rate_%', 'diff_%']].apply(lambda x: round(x,4))

        return df_pv[df_pv['diff_level'].isin(diff_level)]

    if len(lvls_bundle) != 0:
        return drop_rate_hepler(lvls_df)
    return drop_rate_hepler(filtered_df)

def add_board_id(dataframe):
    if dataframe['event_name'] == 'pet_type':
        return '010001'
    elif dataframe['event_name'] == 'chest':
        return '010106'
    else:
        return dataframe['board_id']

def add_step(row1, row2, row3):
    if row1 in ('pet_type', 'chest'):
        return row1
    elif row1 == 'tutorial_step':
        return row1[:8] + '_' + row2[4:] + '_' + row3
    else:
        return row1 + row2

def add_step_id(dataframe):
    if dataframe['event_name'] == 'start_game':
        return '0'
    elif dataframe['event_name'] == 'end_game':
        return '7'
    elif dataframe['event_name'] == 'chest':
        return '0'
    elif dataframe['event_name'] == 'pet_type':
        return '1'
    else:
        return dataframe['step']

def funnel_table(df: pd.DataFrame, app_version: str):
    '''
    Creating funnel table. This table will be used in chart as input data.
    '''
    # filtering DataFrame
    filtered_df = choose_appversion(df=df, app_version=app_version)

    # replacing NULLs with board_id and step_id values
    filtered_df['board_id'] = filtered_df.apply(add_board_id, axis=1)
    filtered_df['step_id'] = filtered_df.apply(add_step_id, axis=1)

    # grouping DataFrame
    df_pv = filtered_df.groupby(by=['event_name','board_id', 'step_id']).agg(
                {"total_users": np.sum}).fillna(0).reset_index()

    # calculating metrics
    df_pv['unique_users_%'] = df_pv['total_users'] / df_pv['total_users'].max() * 100
    df_pv['unique_users_%'] = df_pv['unique_users_%'].apply(lambda x: round(x,2))
    df_pv['step'] = df_pv.apply(lambda row: add_step(row['event_name'],
                                                row['board_id'],
                                                row['step_id']), axis=1)

    df_pv = df_pv[df_pv['step'] != 'tutorial_04_3/2']

    return df_pv.sort_values(by=['board_id', 'step_id'])[:25]

def session_stats(df: pd.DataFrame, app_version: str):
    '''
    Creating session stats. This table will be used in chart as input data.
    '''
    # filtering DataFrame
    filtered_df = choose_appversion(df=df, app_version=app_version)

    # global stats
    global_sess_mean = round(filtered_df['sess_time'].mean() / 60,2)
    global_sess_median = round(filtered_df['sess_time'].median() / 60,2)

    return global_sess_mean, global_sess_median

def session_table(df: pd.DataFrame, app_version: str):
    '''
    Creating session stats. This table will be used in chart as input data.
    '''
    # filtering DataFrame
    filtered_df = choose_appversion(df=df, app_version=app_version)

    # calculating metrics
    df_pvt = filtered_df.groupby('session').agg(
        lambda x: len(x.unique())
            ).reset_index()

    df_pvt['drop'] = round(df_pvt['user_id'] / df_pvt['user_id'].max() * 100, 2)

    return df_pvt[['session', 'drop']]

def economy_table(df: pd.DataFrame, app_version: str, lvls_bundle):
    '''
    Creating economy table. This table will be used in chart as input data.
    '''
    # filtering DataFrame
    filtered_df = choose_appversion(df=df, app_version=app_version)
    lvls_df = filtered_df[filtered_df['levels_bundle'].isin(lvls_bundle)]

    if len(lvls_bundle) != 0:
        return lvls_df.sort_values(by='level')
    return filtered_df.sort_values(by='level')
