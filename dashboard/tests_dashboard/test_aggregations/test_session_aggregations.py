from dashboard.aggregations.session_aggregations import SessionAggregator
import pytest
import pandas as pd 
import numpy as np 
from pandas.testing import assert_frame_equal
from numpy import dtype
from numpy.testing import assert_array_equal

session_events = pd.read_pickle("dataprovider/datasets/query_session.pkl")

@pytest.fixture
def sessagg():
    return SessionAggregator(session_events)

def test_session_events_schema():
    # Setup 
    expected = {
        'user_id': dtype('int64'),
        'app_version': dtype('O'),
        'session': dtype('int64'),
        'sess_time': dtype('float64')
    }

    # Exercise
    result = session_events.dtypes.to_dict()

    # Verify
    assert result == expected

def test_create_session_stats(sessagg):
    # Setup
    _, _, df = sessagg.create_session_stats("0.12")
    _, _, dffloat = sessagg.create_session_stats(0.21)
    expected = ["session", "drop"]

    # Exercise
    df_columns = df.columns.to_list()
    dffloat_columns = df.columns.to_list()

    # Verify
    assert_array_equal(df_columns, expected)
    assert_array_equal(dffloat_columns, expected)

def test_dataframe_empty(sessagg):
    # Setup
    strange_app_version = "Test"

    # Exercise
    _, _, df = sessagg.create_session_stats(strange_app_version)

    # Verify
    assert df.empty == True

