from dashboard.aggregations.winratio_aggregations import WinRatioAggregator
import pytest
import pandas as pd 
import numpy as np 
from pandas.testing import assert_frame_equal
from numpy import dtype

winratio_events = pd.read_pickle("dataprovider/datasets/query_win_ratio.pkl")

def test_winratio_events_schema():
    # Setup 
    expected = {
        'app_version': dtype('O'),
        'levels_bundle': dtype('O'),
        'board_id': dtype('O'),
        'wins': dtype('int64'),
        'loss': dtype('int64'),
        'total_games': dtype('int64'),
        'moves_left': dtype('int64'),
        'iqr': dtype('int64'),
        'median_attempt': dtype('float64')
     }

    # Exercise
    result = winratio_events.dtypes.to_dict()

    # Verify
    assert result == expected

