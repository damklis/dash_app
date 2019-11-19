from dashboard.aggregations.base_aggregations import BaseAggregator
import pytest
import pandas as pd 
import numpy as np 
from pandas.testing import assert_frame_equal

@pytest.fixture
def dataframe():
    data = {
        "app_version" : ["0.21", "0.12", "0.16"],
        "board_id" : ["010101", "010201", "010301"],
        "score" : [11, 23, 45]
    }
    return pd.DataFrame(data)

def test_add_difficulty_level(dataframe):
    # Setup
    base = BaseAggregator(dataframe)
    expected = pd.DataFrame(
        {
        "app_version" : ["0.21", "0.12", "0.16"],
        "board_id" : ["010101", "010201", "010301"],
        "score" : [11, 23, 45],
        "diff_level" : ["normal", "challenging", "expert"]
        }
    )

    # Exercise
    result = base.dataframe
    result["diff_level"] = result["board_id"].apply(
        base.add_difficulty_level
    )

    # Verify
    assert_frame_equal(expected, result)

def test_choose_appversion(dataframe):
    # Setup
    base = BaseAggregator(dataframe)
    expected = pd.DataFrame(
        {
        "app_version" : ["0.21"],
        "board_id" : ["010101"],
        "score" : [11]
        }
    )
    
    # Exercise
    result = base.choose_appversion("0.21")
    result_float = base.choose_appversion(0.21)

    # Verify
    assert_frame_equal(result, expected)
    assert_frame_equal(result_float, expected)
