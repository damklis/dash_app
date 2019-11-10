import pandas as pd
import numpy as np
from factory.aggregations.base_aggregations import BaseAggregator
import math


class WinRatioAgregator(BaseAggregator):

    def __init__(self, dataframe, lvls_bundle, diff_level, randomness):
        super().__init__(dataframe)
        self.lvls_bundle = lvls_bundle
        self.diff_level = diff_level
        self.randomness_level = randomness

    @staticmethod
    def add_randomness_label(column):
        """
        Maps column with randomness level.
        """
        if 0 <= column <= 3:
            return "low"
        elif 3 < column <= 7:
            return "medium"
        else:
            return "high"
    
    def create_winratio_df(self, app_version):
        """
        Creating result table with aggregated values. 
        This table will be used in the chart as input data.
        """
        filtered_df = self.choose_appversion(app_version)
        lvls_df = filtered_df[filtered_df["levels_bundle"].isin(self.lvls_bundle)]

        def win_ratio_helper(df_help):
            df_pv = df_help.groupby("board_id").agg(
                    {"total_games": np.sum,
                    "wins": np.sum,
                    "loss": np.sum,
                    "moves_left":np.mean,
                    "iqr": np.mean,
                    "median_attempt": np.mean
                    }
            ).reset_index()

            ### calculating metrics
            df_pv["loss"] = df_pv["loss"].fillna(0)
            df_pv["win_ratio_%"] = round(df_pv["wins"] / df_pv["total_games"]*100 ,2)
            df_pv["randomness"] = df_pv["iqr"].apply(self.add_randomness_label)
            df_pv["diff_level"] = df_pv["board_id"].apply(self.add_difficulty_level)
            df_pv["moves_left"] = round(df_pv["moves_left"],2)
            df_pv["std_err_%"] = df_pv.apply(
                lambda row: self.calculate_std_err(row), axis=1
                )

            df_pv = df_pv[df_pv["diff_level"].isin(self.diff_level)]

            return df_pv[df_pv["randomness"].isin(self.randomness_level)]

        if len(self.lvls_bundle) != 0:
            return win_ratio_helper(lvls_df)
            
        return win_ratio_helper(filtered_df)

    def calculate_std_err(self, df):
        """
        Returns a standard error.
        """
        num = df["win_ratio_%"] * (100 - df["win_ratio_%"])
        den = df["total_games"]
        std_err = math.sqrt(num/den)
        return round(std_err, 2)