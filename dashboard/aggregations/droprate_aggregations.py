import pandas as pd
import numpy as np
from dashboard.aggregations.base_aggregations import BaseAggregator
import math

class DropRateAggregator(BaseAggregator):

    def __init__(self, dataframe, lvls_bundle, diff_level):
        super().__init__(dataframe)
        self.lvls_bundle = lvls_bundle
        self.diff_level = diff_level

    def calculate_metrics(self, df):
        """
        Returns aggregated pandas DataFrame.
        """
        df_pv = df.groupby(by="board_id").agg(
            {"total_users": np.sum}).fillna(0).reset_index(
        )

        return (df_pv
             .assign(
                diff_level = df_pv["board_id"].apply(self.add_difficulty_level),
                stay_rate = round(df_pv["total_users"]/df_pv["total_users"].max(),4)*100
            ).assign(
                drop_rate = lambda r: 100.00 - r["stay_rate"],
                shift = lambda r: r["drop_rate"].shift(1).fillna(0),
                diff = lambda r: (r["drop_rate"] - r["shift"]).apply(
                    lambda r: 0 if r < 0 else r
                )
            ).where(
                lambda r: r["diff_level"].isin(self.diff_level)
            ).dropna()
             .round({"drop_rate": 2, "stay_rate": 2, "diff": 2})
        )

    def create_drop_rate_df(self, app_version):
        """
        Returns final DataFrame with aggregated values (ex. drop-rate ratio).
        """
        filtered_df = self.choose_appversion(app_version)
        lvls_df = filtered_df[
            filtered_df["levels_bundle"].isin(self.lvls_bundle)
        ]

        if len(self.lvls_bundle) != 0:
            return self.calculate_metrics(lvls_df)

        return self.calculate_metrics(filtered_df)

