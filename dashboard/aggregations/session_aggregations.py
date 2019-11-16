import pandas as pd
import numpy as np
from dashboard.aggregations.base_aggregations import BaseAggregator

class SessionAggregator(BaseAggregator):

    def __init__(self, dataframe):
        super().__init__(dataframe)

    def create_session_stats(self, app_version):
        """
        Returns session stats as tuple.
        These variables will be used in the chart as input data.
        """
        filtered_df = self.choose_appversion(app_version)
        
        ### calculating global session metrics
        glob_sess_mean = round(filtered_df["sess_time"].mean() / 60,2)
        glob_sess_median = round(filtered_df["sess_time"].median() / 60,2)

        return (
            glob_sess_mean,
            glob_sess_median,
            filtered_df
            .groupby("session")
            .agg(
                lambda sess: len(sess.unique())
            )
            .reset_index()
            .assign(
                drop=lambda r: round(r["user_id"]/r["user_id"].max()*100, 2)
            )
            .loc[:, ["session", "drop"]]
        )