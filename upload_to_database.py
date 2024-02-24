import streamlit_authenticator as stauth

import database as db

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
        db.insert_user(username, name, hash_password,email)
    

register("admin", "admin Chauhan", "admin","admin@gmail.com")
