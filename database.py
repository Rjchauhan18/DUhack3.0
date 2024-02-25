import os

from deta import Deta  
from dotenv import load_dotenv  
import streamlit_authenticator as stauth


# Load the environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("User")


def insert_user(username, name, password,email):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username, "name": name, "password": password, "email":email})


def fetch_all_users():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items


def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)


def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)


def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)




def register(username, name, password,email):
    """Returns the user on a successful user creation, otherwise raises and error"""
    usernames = []
    names = []
    passwords = []
    emails = []

    # append user data
    usernames.append(username)
    names.append(name)
    passwords.append(password)
    emails.append(email)

    # convert password to hash password
    hashed_passwords = stauth.Hasher(passwords).generate()


    for (username, name, hash_password,email) in zip(usernames, names, hashed_passwords,emails):
        # db.insert_user(username, name, hash_password)
        insert_user(username, name, hash_password,email)
    
