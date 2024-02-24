import base64
import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest


def preprocess_data(df):
    # Handle missing values by imputing with mean
    imputer = SimpleImputer(strategy='mean')
    df[df.select_dtypes(include=['float64', 'int64']).columns] = imputer.fit_transform(
        df.select_dtypes(include=['float64', 'int64']))

    # Handle outliers using Isolation Forest
    clf = IsolationForest(contamination=0.1)
    outlier_mask = clf.fit_predict(
        df.select_dtypes(include=['float64', 'int64'])) == 1
    df = df[outlier_mask]

    # Encode categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Scale numerical variables
    scaler = StandardScaler()
    df[df.select_dtypes(include=['float64', 'int64']).columns] = scaler.fit_transform(
        df.select_dtypes(include=['float64', 'int64']))

    st.dataframe(df,height=500,width=1000)
    st.download_button(
        label="Download Preprocessed Data as CSV",
        data=df.to_csv(index=False).encode(),
        file_name='preprocessed_data.csv',
        mime='text/csv'
    )
