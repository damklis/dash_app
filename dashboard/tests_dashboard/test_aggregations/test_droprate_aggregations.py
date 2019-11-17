from dashboard.aggregations.droprate_aggregations import DropRateAggregator
import pytest
import pandas as pd 
import numpy as np 
from pandas.testing import assert_frame_equal
from numpy import dtype

droprate_events = pd.read_pickle("dataprovider/datasets/query_drop_rate.pkl")

def test_droprate_events_schema():
    # Setup 
    expected = {
        'board_id': dtype('O'),
        'total_users': dtype('int64'),
        'app_version': dtype('O'),
        'levels_bundle': dtype('O')
    }

    # Exercise
    result = droprate_events.dtypes.to_dict()

    # Verify
    assert result == expected

