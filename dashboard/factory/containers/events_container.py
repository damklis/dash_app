from dataclasses import dataclass
import pandas as pd

@dataclass
class EventsContainer:

    win_lose : pd.DataFrame
    drop_rate : pd.DataFrame
    funnel : pd.DataFrame
    session : pd.DataFrame
    economy : pd.DataFrame
    economy_2 : pd.DataFrame

    def get_n_last_versions(self, n_value=2):
        """
        Extracts last n global versions of application.
        Returns tuple with n items.
        """
        list_of_versions = sorted(
            self.funnel["app_version"].unique().tolist(),
            reverse=True
        )
        
        return tuple(list_of_versions[:n_value])

