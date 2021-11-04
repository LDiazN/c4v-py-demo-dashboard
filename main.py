"""
    Entry point for the streamlit app
"""
import streamlit as sl
import app

sl.write("# 🔬 C4V Microscope")
sl.write("In the following dashboard we will see how the scraping, crawling and classification works.")

app = app.App()

# Add a title to the sidebar
sl.sidebar.write("## Filters")
sl.sidebar.write("Specify which data you want to see with the following filters")

# Add a selector to filter by label 
label = sl.sidebar.selectbox("Label: ", options=app.label_options, help="Label assigned by the classifier")
scraped = sl.sidebar.selectbox("Scraped: ", options=app.scraped_options, help="Whether the instance data is complete or not")
use_max_rows = sl.sidebar.checkbox("Limit Rows: ", value=True, help="Max ammount of rows to show")\

# If limiting the max amount of rows, then ask for a max value
if use_max_rows:
    max_rows = sl.sidebar.number_input("Max: ", 0, value=100, help="Maximum amount of rows to retrieve and show")
else:
    max_rows = -1

sl.dataframe(app.get_dashboard_data(label=label, max_rows=max_rows))

