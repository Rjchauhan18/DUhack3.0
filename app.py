import streamlit as st
import pandas as pd
# from DataPreProcessing import preprocess_data
from Datasets import Datasets
from Model import ModelTrainer
from Visualization import Visualization

# Database Connectivity Modelus
import streamlit_authenticator as stauth  
import database as db
from upload_to_database import register


# Set page title and favicon
st.set_page_config(page_title="Machine Learning Automation", page_icon=":robot:")

# --- USER AUTHENTICATION ---
i=0
if i not in st.session_state:
    st.session_state.i = 0

if st.session_state.i == 0:
    st.session_state.i += 1
    try:
            
        users = db.fetch_all_users()

        usernames = [user["key"] for user in users]
        names = [user["name"] for user in users]
        hashed_passwords = [user["password"] for user in users]

        credentials = {"usernames":{}}

        for un, name, pw in zip(usernames, names, hashed_passwords):
            user_dict = {"name":name,"password":pw}
            credentials["usernames"].update({un:user_dict})
    except Exception as e:
        st.info(f"Error: {e}, Please refresh the page or try again later.")
        st.stop()

authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)

# authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"ML Automation", "abcdef", cookie_expiry_days=30)

def registration():
    # Registration form
    st.subheader('Registration')
    with st.form(key='Sign Up'):
        username = st.text_input('Username')
        name = st.text_input('Name')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        reenter_password = st.text_input('Re-enter Password', type='password')

        if st.form_submit_button('Sign Up'):

            if password != reenter_password:
                st.error('Passwords do not match')
            else:

                # Save user registration details to database
                try:
                    # db.save_user(username, name, password, email)
                    register(username, name, password, email)
                    st.success('SignUp successful! Please login to access the application.')
                except Exception as e:
                    st.error(f"Error: {e}")

# Created placeholder for login and signup form to maintain them in tab
placeholder = st.empty()    

with placeholder:
    Login, Sign_Up = st.tabs(["Login", "Sing Up"])

with Login:
    name, authentication_status, username = authenticator.login()

if authentication_status == None or authentication_status == False:
    with Sign_Up:
        if authentication_status == None or authentication_status == False:
            registration()


if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    placeholder.empty()

    # Title of the application
    st.title('Machine Learning Automation')

    # Load dataset
    with st.sidebar:

        st.write(f"Welcome {name}")
        authenticator.logout("Logout", "sidebar")

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
