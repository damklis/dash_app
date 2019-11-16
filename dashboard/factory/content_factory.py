from dashboard.containers.events_container import EventsContainer
from dashboard.aggregations.funnel_aggregations import FunnelAggregator
from dashboard.aggregations.session_aggregations import SessionAggregator
from dashboard.aggregations.winratio_aggregations import WinRatioAggregator
from dashboard.aggregations.droprate_aggregations import DropRateAggregator
from dashboard.aggregations.economy_aggregations import EconomyAggregator

class ContentFactory(object):

    def __init__(self, events, app, diff_dr,
        diff_wr, randomness, resource, data, lvls):
        self.app_version = app
        self.resource = resource
        self.df_data = data
        self.randomness_label = randomness
        self.dr = DropRateAggregator(events.drop_rate, lvls, diff_dr)
        self.wr = WinRatioAggregator(events.win_lose, lvls, diff_wr, randomness)
        self.ec = EconomyAggregator(events.economy, lvls)
        self.ec2 = EconomyAggregator(events.economy_2, lvls)
        self.sess = SessionAggregator(events.session)
        self.fun = FunnelAggregator(events.funnel)
        _fst_vers, _snd_vers = events.get_n_last_versions(2)

        if self.app_version == _fst_vers:
            self.app_version_2 = _snd_vers
        else:
            self.app_version_2 = _fst_vers 

    @property
    def funnel_df(self):
        """
        Returns dataframe necessary for frst funnel chart.
        """
        return self.fun.create_funnel_df(self.app_version)
    
    @property
    def funnel_2_df(self):
        """
        Returns dataframe necessary for second funnel chart.
        """
        return self.fun.create_funnel_df(self.app_version_2)

    @property
    def session_stats(self):
        """
        Returns data necessary for session charts.
        """
        return self.sess.create_session_stats(self.app_version)

    @property
    def win_ratio_df(self):
        """
        Returns dataframe necessary for win-ratio chart.
        """
        return self.wr.create_winratio_df(self.app_version)

    @property
    def drop_rate_df(self):
        """
        Returns dataframe necessary for drop-rate chart.
        """
        return self.dr.create_drop_rate_df(self.app_version)

    @property
    def economy_df(self):
        """
        Returns dataframe necessary for first economy chart.
        """
        return self.ec.create_economy_df(self.app_version)

    @property
    def economy_2_df(self):
        """
        Returns dataframe necessary for second economy chart.
        """
        return self.ec2.create_economy_df(self.app_version)                        
