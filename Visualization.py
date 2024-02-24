import streamlit as st
import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
# from weasyprint import HTML

def Visualization(data):
    st.title("Visualization of Models")
    # pd.DataFrame(data)
    pf = ProfileReport(data)
    st_profile_report(pf)
    export = pf.to_html()
    st.download_button(label="Download Full Report", data=export, file_name='report.html')
    
   