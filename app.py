"""
    State for the application, computing the data to show
"""
# Local imports
from typing import List
import c4v.microscope as ms
import config         as c

# Python imports
import logging as log
from pathlib import Path

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

        self._config = config

    @property
    def config(self) -> c.Config:
        """
            Configuration used by this manager object
        """
        return self._config

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

    @property
    def available_branchs(self) -> List[str]:
        """
            List of available branches
        """
        # TODO add a function to classifier object to get available experiments and branches for an experiment
        experiments_path = Path(self._manager.local_files_path, "experiments")
        return [str(x.name) for x in experiments_path.glob("*")]

    def available_experiments_for_branch(self, branch_name : str) -> List[str]:
        """
            List of available experiments for a given branch. Raise an error if invalid branch name is provided.

            # Parameters
                - branch_name : `str` = branch whose experiments are to be retrieved
            # Return
                List of experiments corresponding to the given branch
        """
        assert branch_name in self.available_branchs

        # TODO add function to the classifier object to get experiments from branch
        experiments_path = Path(self._manager.local_files_path, "experiments", branch_name)

        return [str(x.name) for x in experiments_path.glob("*")]

    def experiment_summary(self, branch_name : str, experiment_name : str) -> str:
        """
            Summary for the given experiment defined by its branch name and experiment name. Might be None if 
            no summary is found
            # Parameters
                - branch_name : `str ` = Branch name for experiment
                - experiment_name : `str ` = Experiment name for experiment
            # Return
                Summary for the given experiment, or None if not found
        """
        # Sanity check
        assert branch_name in self.available_branchs
        assert experiment_name in self.available_experiments_for_branch(branch_name)

        # TODO Crear funcion en c4v manager que traiga el summary
        summary_path = Path(self._manager.local_files_path, "experiments", branch_name, experiment_name, "summary.txt")

        # Return None if not exists
        if not summary_path.exists():
            return None

        return summary_path.read_text()

    def classify(self, branch_name : str, experiment_name : str, limit : int = -1):
        """
            Run a classification process.
            # Parameters
                - branch_name : `str ` = Branch name for experiment
                - experiment_name : `str ` = Experiment name for experiment
                - limit  : `int` = Max ammount of rows to classify, provide a negative number for no limit
        """
        self._manager.run_pending_classification_from_experiment(branch_name, experiment_name, limit=limit)