from factory.containers.events_container import EventsContainer
from factory.aggregations.funnel_aggregations import FunnelAggregator
from factory.aggregations.session_aggregations import SessionAgregator
from factory.aggregations.winratio_aggregations import WinRatioAgregator
from factory.aggregations.droprate_aggregations import DropRateAgregator
from factory.aggregations.economy_aggregations import EconomyAgregator
import json

class ContentFactory(object):

    def __init__(self, events, app, diff_dr,
        diff_wr, randomness, resource, data, lvls):

        self._dfs = events
        self.app_version = app
        self.diff_lvl_dr, self.diff_lvl_wr = diff_dr, diff_wr
        self.randomness_label = randomness
        self.resource = resource
        self.df_data = data
        self.lvls = lvls
        self._fst_vers, self._snd_vers = self._dfs.get_n_last_versions()

        if self.app_version == self._fst_vers:
            self.app_version_2 = self._snd_vers
        else:
            self.app_version_2 = self._fst_vers 

    @property
    def funnel_df(self):
        """
        Returns dataframe necessary for frst funnel chart.
        """
        funnel = FunnelAggregator(self._dfs.funnel, self.app_version)
        return funnel.create_funnel_df()
    
    @property
    def funnel_2_df(self):
        """
        Returns dataframe necessary for second funnel chart.
        """
        funnel = FunnelAggregator(self._dfs.funnel, self.app_version_2)
        return funnel.create_funnel_df()

    @property
    def session_stats(self):
        """
        Returns data necessary for session charts.
        """
        sess = SessionAgregator(self._dfs.session, self.app_version)
        return sess.create_session_stats()

    @property
    def win_ratio_df(self):
        """
        Returns dataframe necessary for win-ratio chart.
        """
        winratio = WinRatioAgregator(self._dfs.win_lose, self.app_version)
        return winratio.create_winratio_df(
            self.lvls, self.diff_lvl_wr, self.randomness_label
        )

    @property
    def drop_rate_df(self):
        """
        Returns dataframe necessary for drop-rate chart.
        """
        droprate = DropRateAgregator(self._dfs.drop_rate, self.app_version)
        return droprate.create_drop_rate_df(
            self.lvls, self.diff_lvl_wr
        )

    @property
    def economy_df(self):
        """
        Returns dataframe necessary for first economy chart.
        """
        ec = EconomyAgregator(self._dfs.economy, self.app_version)
        return ec.create_economy_df(self.lvls)

    @property
    def economy_2_df(self):
        """
        Returns dataframe necessary for second economy chart.
        """
        ec = EconomyAgregator(self._dfs.economy_2, self.app_version)
        return ec.create_economy_df(self.lvls)
