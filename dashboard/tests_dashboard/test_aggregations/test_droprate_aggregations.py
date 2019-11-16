from dashboard.aggregations.droprate_aggregations import DropRateAgregator
import pytest
import pandas as pd 
import numpy as np 
from pandas.testing import assert_frame_equal

droprate_events = pd.read_pickle("dataprovider/datasets/query_drop_rate.pkl")

@pytest.mark.parametrize("provided,expected", [
    (["normal", "challenging", "expert"], 3),
    (["normal", "challenging"], 2),
    (["normal"], 1)
])
def test_calclate_metrics_with_diff_levels(provided, expected):
    # Setup
    dr_agg = DropRateAgregator(droprate_events, [], provided)

    # Exercise
    df = dr_agg.calclate_metrics(droprate_events)
    result = len(df["diff_level"].unique())

    # Verify
    assert result == expected

