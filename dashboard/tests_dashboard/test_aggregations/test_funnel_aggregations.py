from dashboard.aggregations.funnel_aggregations import FunnelAggregator
import pytest
import pandas as pd 
import numpy as np 
from pandas.testing import assert_frame_equal
from numpy import dtype

funnel_events = pd.read_pickle("dataprovider/datasets/query_funnel.pkl")

def test_funnel_events_schema():
    # Setup 
    expected = {
        'event_name': dtype('O'),
        'board_id': dtype('O'),
        'total_users': dtype('int64'),
        'app_version': dtype('O'),
        'step': dtype('O')
    }

    # Exercise
    result = funnel_events.dtypes.to_dict()

    # Verify
    assert result == expected

@pytest.fixture
def funnagg():
    return FunnelAggregator(funnel_events)

def test_create_funnel_df(funnagg):
    # Setup
    strange_app_version = "0.11111111x"

    # Exercise/Verify
    with pytest.raises(ValueError):
        funnagg.create_funnel_df(strange_app_version)
