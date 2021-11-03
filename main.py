"""
    Entry point for the streamlit app
"""
import streamlit as sl
import app

sl.write("# 🔬 C4V Microscope")
sl.write("In the following dashboard we will see how the scraping, crawling and classification works.")

app_instance = app.App()

sl.write("hellooooooo")