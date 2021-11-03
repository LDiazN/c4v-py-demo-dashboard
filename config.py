"""
    This file contains a class for the app configuration.
    It gets configured once the app starts using the environment 
    variables as a configuration
"""

# Python imports
import os
import enum

class EnvOptions(enum.Enum):
    C4V_DB_BACKEND : str = "SQLITE" 

class Config:
    """
        App configuration State
    """

    # db to use when requesting for stored data
    default_db_backend : str = EnvOptions.C4V_DB_BACKEND.value

    def __init__(self, db_backend : str = None):
        # Set up db backend
        self._db_backend =  db_backend or \
                            os.environ.get(
                                EnvOptions.C4V_DB_BACKEND.value
                            )
        
    @property
    def db_backend(self) -> str:
        """
            Configured db backend
        """
        return self._db_backend or self.default_db_backend
