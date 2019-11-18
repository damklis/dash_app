
import pandas as pd
import numpy as np
from dashboard.aggregations.base_aggregations import BaseAggregator


class FunnelAggregator(BaseAggregator):

    def __init__(self, dataframe):
        super().__init__(dataframe)
        self.max_steps = 25

    def add_board_id(self, df):
        """
        Maps event name and board_id code.
        """
        if df["event_name"] == "pet_type":
            return "010001"
        elif  df["event_name"] == "chest":
            return "010106"
        else:
            return  df["board_id"]
    
    def add_step_id(self, df):
        """
        Maps event name and step id code.
        """
        if df["event_name"] == "start_game":
            return "0"
        elif df["event_name"] == "end_game":
            return "7"
        elif df["event_name"] == "chest":
            return "0"
        elif df["event_name"] == "pet_type":
            return "1"
        else:
            return df["step"]

    def add_step(self, df):
        """
        Maps event name, board_id and returns step.
        """
        if df["event_name"] in ("pet_type", "chest"):
            return df["event_name"]
        elif df["event_name"] == "tutorial_step":
            name = df["event_name"][:8]
            level = df["board_id"][4:]
            step_id = df["step_id"]
            return "_".join([name, level, step_id])
        else:
            return df["event_name"] + df["board_id"]

    def create_funnel_df(self, app_version):
        """
        Creating funnel table with aggregated values.
        This table will be used in the chart as input data.
        """
        filtered_df = self.choose_appversion(app_version)

        return (filtered_df
             .assign(
                board_id = filtered_df.apply(self.add_board_id, axis=1),
                step_id = filtered_df.apply(self.add_step_id, axis=1)
            ).groupby(
                by=["event_name","board_id", "step_id"]
            ).agg(
                {"total_users": np.sum}
            ).fillna(0)
             .reset_index()
             .assign(
                unique_users = lambda r: round(r["total_users"]/r["total_users"].max(),4)*100,
                step = lambda r: r.apply(self.add_step, axis=1)
            ).sort_values(by=["board_id", "step_id"])[:self.max_steps]
        )