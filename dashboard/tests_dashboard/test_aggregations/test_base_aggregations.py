from dashboard.aggregations.base_aggregations import BaseAggregator
import pytest
import pandas as pd 
import numpy as np 
from pandas.testing import assert_frame_equal

@pytest.fixture
def dataframe():
    data = {
        "app_version" : ["0.10", "0.12", "0.16"],
        "board_id" : ["010101", "010201", "010301"],
        "score" : [11, 23, 45]
    }
    return pd.DataFrame(data)

def test_add_difficulty_level(dataframe):
    # Setup
    base = BaseAggregator(dataframe)
    expected = pd.DataFrame(
        {
        "app_version" : ["0.10", "0.12", "0.16"],
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

@pytest.mark.parametrize("provided,expected", [
    ("", 3),
    (["normal", "challenging"], 2),
    (["normal"], 1)
])
def test_choose_appversion(dataframe):

