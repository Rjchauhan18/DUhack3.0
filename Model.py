import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from pycaret.classification import *
from pycaret.regression import *

def ModelTrainer(data):
     # Choose target variable
    target = st.selectbox("Select target variable", data.columns)
    
    # Drop rows with missing target values
    data.dropna(subset=[target], inplace=True)
    
    # Choose task type
    task_type = st.radio("Select task type:", ("Classification", "Regression"))
    if task_type == "Classification":
        categorical_cols = [
            col for col in data.columns if data[col].dtype == 'object']
        numerical_cols = [
            col for col in data.columns if col not in categorical_cols]
        preprocessor = ColumnTransformer(transformers=[
            ('num', SimpleImputer(strategy='median'), numerical_cols),
            ('cat', Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ]), categorical_cols)
        ])
    else:
        numerical_cols = [
            col for col in data.columns if data[col].dtype in ['int64', 'float64']]
        preprocessor = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

    # Model Building
    st.subheader('Model Building')
    categorical_cols = data.select_dtypes(include='category').columns
    print("Categorical Columns:", categorical_cols)
    if st.button('Build Model'):
    # Build model based on task type
        if task_type == "Classification":
            setup(data=data, target=target, preprocess=preprocessor)
            models = compare_models()  # Get all models
            temp = pull()
            st.write(temp)
        else:
            setup(data=data, target=target, preprocess=preprocessor,index=False)
            models = compare_models()  # Get all models
            temp = pull()
            st.write(temp)