"""
    Entry point for the streamlit app
"""
import streamlit as sl
import app

sl.write("# 🔬 C4V Microscope")
sl.write("In the following dashboard we will see how the scraping, crawling and classification works.")

app = app.App()

# -- < Filtering > ---------------------------------------------
# Add a title to the sidebar
sl.sidebar.write("## Filters")
sl.sidebar.write("Specify which data you want to see with the following filters")

# Add a selector to filter by label 
label = sl.sidebar.selectbox("Label: ", options=app.label_options, help="Label assigned by the classifier")
scraped = sl.sidebar.selectbox("Scraped: ", options=app.scraped_options, help="Whether the instance data is complete or not")
use_max_rows = sl.sidebar.checkbox("Limit Rows: ", value=True, help="Max ammount of rows to show")\

# -- < Row Limits > -------------------------------------------
# If limiting the max amount of rows, then ask for a max value
if use_max_rows:
    max_rows = sl.sidebar.number_input("Max: ", 0, value=100, help="Maximum amount of rows to retrieve and show")
else:
    max_rows = -1

# -- < Classification controls > ------------------------------
# Help Message
sl.sidebar.write("-----")
sl.sidebar.write("## Classification controls")
sl.sidebar.write("Run a classification process, select parameters with the following controls.")

# Branch names
NO_BRANCH_NAME = "No Branch"
branch_name = sl.sidebar.selectbox("Branch: ", [NO_BRANCH_NAME] + app.available_branchs, help="Experiment branch to select a classifier model from") 
experiment_options = [] if branch_name == NO_BRANCH_NAME else app.available_experiments_for_branch(branch_name)
experiment_name = sl.sidebar.selectbox("Experiment: ", experiment_options, help="Experiment name corresponding to provided branch")

# Description for experiment if provided
if experiment_name:
    sl.sidebar.write("### Summary for this experiment: ")
    sl.sidebar.text_area("Summary", app.experiment_summary(branch_name, experiment_name), height=100)

# Set limits
use_classiffication_limit = sl.sidebar.checkbox("Limit", value=True, help="Max ammount of rows to use during classification. Might be useful if you're running out of memory")
if use_classiffication_limit:
    max_rows_to_classify = sl.sidebar.number_input("Max rows", 0, value=100, help="Max amount of rows to classify. If you want no limit, uncheck the checkbox above")
else:
    max_rows_to_classify = -1

# Run classification button
def run_classification_callback():
    if not experiment_name:
        sl.warning("No experiment set up. Select one to choose a classifier model to use during classification")        
    else:
        sl.info("Running classification process, this may take a while...")
        try:
            app.classify(branch_name, experiment_name, max_rows_to_classify)
        except Exception as e:
            sl.error(   f"Unable to classify using model {branch_name}/{experiment_name} {('and up to ' + str(max_rows_to_classify)) if max_rows_to_classify >= 0 else ''}.    " + \
                        f"Error: {e}"
                    )

sl.sidebar.button("Classify", help="Perform the classification process", on_click=run_classification_callback)

# -- < Show Dashboard > ---------------------------------------
sl.dataframe(app.get_dashboard_data(label=label, max_rows=max_rows))

