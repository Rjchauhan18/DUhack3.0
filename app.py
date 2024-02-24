import streamlit as st
import pandas as pd
from DataPreProcessing import preprocess_data
from Datasets import Datasets
from Model import ModelTrainer
from Visualization import Visualization

# Set page title and favicon
st.set_page_config(page_title="Machine Learning Automation", page_icon=":robot:")

# Title of the application
st.title('Machine Learning Automation')

# Load dataset
with st.sidebar:
    st.sidebar.title("Machine Learning Menu")
    st.sidebar.info("Select an option from below:")
    select = st.selectbox("", ['Dataset', 'Data Preprocessing',
                                    'Model Training', 'Visualization of Models'])

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load dataset
    data = pd.read_csv(uploaded_file, index_col=0)
    
    # Display the dataset
    st.write("### Uploaded Dataset:")
    st.dataframe(data,height=450,width=800)
    
   

if select == "Model Training":
    if uploaded_file is not None:
        ModelTrainer(data)

if select == "Data Preprocessing":
    if uploaded_file is not None:
        preprocess_data(data)

if select == "Datasets":
    # TODO: Datasets
    Datasets()

if select == "Visualization of Models":
    # TODO: Visualization of models
    Visualization(data)
