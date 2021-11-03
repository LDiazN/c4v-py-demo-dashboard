"""
    State for the application, computing the data to show
"""
# Local imports
import c4v.microscope as ms
import config         as c

# Python imports
import logging as log

# Third party imports
import pandas as pd

class App:
    """
        Main application object, mainly used to get the data to show in the front end
    """

    def __init__(self, config : c.Config = c.Config()) -> None:
        # create persistency manager based on the specified backend
        if config.db_backend == c.DBBackEndOptions.SQLITE.value:
            self._manager = ms.Manager.from_default()
        else:
            raise NotImplementedError(f"DB Backend '{config.db_backend}' not yet implemented")

    def get_dashboard_data(self, max_rows : int = 100) -> pd.DataFrame:
        """
            Get data to show in the dashboard
            # Parameters:   
                - max_rows : `int` = (optional) maximum amount of rows to display
        """
        return pd.DataFrame(list(self._manager.get_all(limit=max_rows)))

        

