import pandas as pd
import numpy as np
from factory.aggregations.base_aggregations import BaseAggregator
import math


class DropRateAgregator(BaseAggregator):

    def __init__(self, dataframe, lvls_bundle, diff_level):
        super().__init__(dataframe)
        self.lvls_bundle = lvls_bundle
        self.diff_level = diff_level

    def calclate_metrics(self, df):
        """
        Returns aggregated pandas DataFrame.
        """

        df_pv = df.groupby(by="board_id").agg(
                    {"total_users": np.sum}).fillna(0).reset_index()

        ### calculating metrics
        df_pv["diff_level"] = df_pv["board_id"].apply(self.add_difficulty_level)
        df_pv["stay_rate_%"] = round(df_pv["total_users"] / df_pv["total_users"].max(),4)*100
        df_pv["drop_rate_%"] = 100.00 - df_pv["stay_rate_%"]
        df_pv["shift"] = df_pv["drop_rate_%"].shift(1).fillna(0)
        df_pv["diff_%"] = df_pv["drop_rate_%"] - df_pv["shift"]
        df_pv["diff_%"] = df_pv["diff_%"].apply(lambda x: 0 if x < 0 else x)
        df_pv[["drop_rate_%", "stay_rate_%", "diff_%"]] = df_pv[["drop_rate_%",
            "stay_rate_%", "diff_%"]].apply(lambda x: round(x,4))

        return df_pv[df_pv["diff_level"].isin(self.diff_level)]

    def create_drop_rate_df(self, app_version):
        """
        Returns final DataFrame with aggregated values (ex. drop-rate ratio).
        """

        filtered_df = self.choose_appversion(app_version)
        lvls_df = filtered_df[
            filtered_df["levels_bundle"].isin(self.lvls_bundle)
        ]

        if len(self.lvls_bundle) != 0:
            return self.calclate_metrics(lvls_df)

        return self.calclate_metrics(filtered_df)

    