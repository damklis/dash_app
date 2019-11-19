import pandas as pd
import numpy as np
from dashboard.aggregations.base_aggregations import BaseAggregator
import math


class EconomyAggregator(BaseAggregator):

    def __init__(self, dataframe, lvls_bundle):
        super().__init__(dataframe)
        self.lvls_bundle = lvls_bundle

    def create_economy_df(self, app_version):
        """
        Returns economy table with aggregated values.
        This table will be used in the chart as input data.
        """
        filtered_df = self.choose_appversion(app_version)
        lvls_df = filtered_df.where(
            lambda r: r["levels_bundle"].isin(self.lvls_bundle)
        )

        if len(self.lvls_bundle) != 0:
            return lvls_df.sort_values(by="level")

        return filtered_df.sort_values(by="level")