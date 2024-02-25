import streamlit as st
import pandas as pd
import json
from Data_Pre_Processing import preprocess_data
from Datasets import Datasets
from Model import ModelTrainer
from Visualization import Visualization
from streamlit_lottie import st_lottie
import requests
# Database Connectivity Modules
import streamlit_authenticator as stauth  
import database as db



# Set page title and favicon
st.set_page_config(
    page_title="Auto Craft Ml",
    page_icon="🤖",
    layout="wide",
    
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
# st.set_page_config(page_title="AutoCraftMl", page_icon=":robot:")

#function for lottie animation using request 
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return json.loads(r.text)

def load_lottie_file(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)





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
                    db.register(username, name, password, email)
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
    st.title('🤖Machine Learning Automation')
    # lottie_hi=load_lottie_url('https://app.lottiefiles.com/share/aa673afc-ab71-4a85-b7da-c17a10e3366d')
    # st_lottie(lottie_hi)

    # Load dataset
    with st.sidebar:
        st.write("# Welcome , ")
        st.title(f'{name}👋')
        hi_lottie=load_lottie_file('/home/rahul/Desktop/DUhack3.0/DUhack3.0/lottie_animation/App__sidebar_logo.json')
        st_lottie(hi_lottie)


        select = st.selectbox("Machine Learning Menu", ['Dataset','Dataset Report', 'Data Preprocessing',
                                        'Model Training'])
        authenticator.logout("Logout", "sidebar")

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
        # : Datasets
        Datasets()

    if select == "Visualization of Models":
        # : Visualization of models
        Visualization(data)
