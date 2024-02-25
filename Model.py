import pickle
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from pycaret.classification import setup as cl_setup, pull as cl_pull, compare_models as cl_compare_models, finalize_model as cl_finalize_model
from pycaret.regression import setup as reg_setup, pull as reg_pull, compare_models as reg_compare_models, finalize_model as reg_finalize_model


def ModelTrainer(data):
     # Choose target variable
    target = st.selectbox("Select target variable", data.columns)
    
    # Drop rh missing target values
    data.dropna(subset=[target], inplace=True)
    
    # Choose task type
    task_type = st.radio("Select task type:", ("Classification", "Regression"))
    if target not in data.columns:
        st.error(f"Target variable '{target}' not found in the data.")
        return

    # Get list of numerical and categorical columns
    numerical_features = data.select_dtypes(
        include=['int64', 'float64']).columns.tolist()
    categorical_features = data.select_dtypes(
        include=['object', 'bool', 'category']).columns.tolist()

    # Remove target variable from the lists if present
    numerical_features = [col for col in numerical_features if col != target]
    categorical_features = [
        col for col in categorical_features if col != target]

    # Encode target variable if it's categorical
    if data[target].dtype == 'object':
        label_encoder = LabelEncoder()
        data[target] = label_encoder.fit_transform(data[target])

    # Model Building
    st.subheader('Model Building')
    if st.button('Build Model'):

        # Build model based on task type
        if task_type == "Classification":
            with st.spinner('Training Classification Models...'):
                cl_setup(data=data, target=target, preprocess=True, train_size=0.33, remove_outliers=True,
                         numeric_features=numerical_features, categorical_features=categorical_features, use_gpu=True)
                models = cl_compare_models()  # Get all models
                model_comparison_results = cl_pull()
        else:
            with st.spinner('Training Regression Models...'):
                reg_setup(data=data, target=target, preprocess=True, train_size=0.33, remove_outliers=True,
                          numeric_features=numerical_features, categorical_features=categorical_features, use_gpu=True)
                models = reg_compare_models()  # Get all models
                model_comparison_results = reg_pull()

        # Display the results
        st.write(model_comparison_results)

        # Finalize the best model
        finalized_model = cl_finalize_model(
            models) if task_type == "Classification" else reg_finalize_model(models)

        # Save the finalized model to a pickle file
        with open('best_model.pkl', 'wb') as f:
            pickle.dump(finalized_model, f)

        # Provide a download button for the pickle file
        st.download_button(
            label="Download the best model",
            data=open('best_model.pkl', 'rb'),
            file_name='best_model.pkl',
            mime='application/octet-stream'
        )
