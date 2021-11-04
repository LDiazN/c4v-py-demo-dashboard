"""
    State for the application, computing the data to show
"""
# Local imports
from typing import List
import c4v.microscope as ms
import config         as c

# Python imports
import logging as log

# Third party imports
import pandas as pd
import streamlit as sl
class App:
    """
        Main application object, mainly used to get the data to show in the front end
    """

    # Valid options for labels
    label_options : List[str] = ["ANY", "IRRELEVANTE", "PROBLEMA DEL SERVICIO", "NO LABEL"]

    # Valid options for scraped
    scraped_options : List[str] = ["Any","Yes", "No"]

    def __init__(self, config : c.Config = c.Config()) -> None:
        # create persistency manager based on the specified backend
        if config.db_backend == c.DBBackEndOptions.SQLITE.value:
            self._manager = ms.Manager.from_default()
        else:
            raise NotImplementedError(f"DB Backend '{config.db_backend}' not yet implemented")

    @sl.cache
    def get_dashboard_data(self, max_rows : int = 100, max_content_len : int = 200, label : str = "ANY", scraped : str = "Any") -> pd.DataFrame:
        """
            Get data to show in the dashboard
            # Parameters:   
                - max_rows : `int` = (optional) maximum amount of rows to display
                - max_content_len : `int` = (optional) maximum amount of chars to show in the content field which might be long
                - label : `str` = (optional) description of the label that every instance should have
                - scraped : `str` = (optional) if the instances should be scraped. 
        """
        # Some sanity check
        assert label in App.label_options, f"invalid label: {label}"
        assert scraped in App.scraped_options, f"invalid scraped option: {scraped}"

        # get value depending on if the instances should be scraped
        opt_2_val = {
            "Any" : None,
            "Yes" : True,
            "No"  : False
        }

        query = self._manager.get_all(scraped=opt_2_val[scraped])

        # Add filtering
        if label == "NO LABEL":
            query = (x for x in query if not x.label)
        elif label != "ANY":
            query = (x for x in query if x.label and x.label.value == label)


        elems = []
        for d in query:
            
            # Reformat enum fields
            if d.source: d.source = d.source.value
            if d.label:  d.label  = d.label.value

            # truncate body if needed
            content_len = len(d.content)
            d.content = d.content if content_len < max_content_len else d.content[:max_content_len] + "..."
            elems.append(d)

            # break if gathered enough rows
            if len(elems) == max_rows:
                break

            

        return pd.DataFrame(elems)

        

