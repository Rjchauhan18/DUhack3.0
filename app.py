import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from pycaret.classification import setup as clf_setup, compare_models as clf_compare_models, predict_model as clf_predict_model
from pycaret.regression import setup as reg_setup, compare_models as reg_compare_models, predict_model as reg_predict_model

st.title('ML Automation')

# Load dataset
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
with st.sidebar:
    st.title("ML")
    st.info("Select fields")
    select = st.selectbox("Select Below", ['Upload Dataset', 'Data Preprocess',
                          'Model Selection/Specification', 'Visualization of Models', 'Download Model'])

if select == 'Upload Dataset':
    if uploaded_file is not None:
        # Load dataset
        data = pd.read_csv(uploaded_file)

        # Display the dataset
        st.write(data)

        # Choose target variable
        target = st.selectbox("Select target variable", data.columns)

        # Drop rows with missing target values
        data.dropna(subset=[target], inplace=True)

        # Choose task type
        task_type = st.radio("Select task type:",
                             ("Classification", "Regression"))

        # Preprocessing pipeline
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
if st.button('Build Model'):
    # Build model based on task type
    if task_type == "Classification":
        clf_setup(data=data, target=target, preprocess=preprocessor)
        models = clf_compare_models() 
        
    else:
        reg_setup(data=data, target=target, preprocess=preprocessor)
        models = reg_compare_models()
        st.write(models)# Get all models

    st.write("Model Comparison:")
    