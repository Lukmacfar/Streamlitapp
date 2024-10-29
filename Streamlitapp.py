import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
from streamlit_option_menu import option_menu

upload_data_page = st.Page(
    page = "page1.py",
    title = "Upload Data",
    default = True
)
Trigger_page = st.Page(
    page = "page2.py",
    title = "Trigger Page",
    default = False
)

pg = st.navigation(pages = [upload_data_page,Trigger_page],position= "sidebar")
pg.run()  




