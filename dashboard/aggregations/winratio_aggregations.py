import pandas as pd
import numpy as np
from dashboard.aggregations.base_aggregations import BaseAggregator
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

    def calculate_metrics(self, df):
        """
        Returns aggregated pandas DataFrame.
        """
        df_pv = df.groupby("board_id").agg(
                {"total_games": np.sum,
                "wins": np.sum,
                "loss": np.sum,
                "moves_left":np.mean,
                "iqr": np.mean,
                "median_attempt": np.mean
                }
        ).reset_index()
        
        return (df_pv
            .fillna(0)
            .assign(
                win_ratio = round(df_pv["wins"]/df_pv["total_games"]*100 ,2),
                randomness = df_pv["iqr"].apply(self.add_randomness_label),
                diff_level = df_pv["board_id"].apply(self.add_difficulty_level),
            ).assign(
                std_err = lambda r: r.apply(self.calculate_std_err, axis=1)
            ).where(
                lambda r: r["diff_level"].isin(self.diff_level)
            ).where(
                lambda r: r["randomness"].isin(self.randomness_level)
            ).dropna()
        )
    
    def create_winratio_df(self, app_version):
        """
        Creating result table with aggregated values. 
        This table will be used in the chart as input data.
        """
        filtered_df = self.choose_appversion(app_version)
        lvls_df = filtered_df[
            filtered_df["levels_bundle"].isin(self.lvls_bundle)
        ]

        if len(self.lvls_bundle) != 0:
            return self.calculate_metrics(lvls_df)
            
        return self.calculate_metrics(filtered_df)

    def calculate_std_err(self, df):
        """
        Returns a standard error.
        """
        num = df["win_ratio"] * (100 - df["win_ratio"])
        den = df["total_games"]
        std_err = math.sqrt(num/den)
        return round(std_err, 2)