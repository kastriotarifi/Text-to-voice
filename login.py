import streamlit as st
import streamlit_authenticator as stauth

# Define credentials
credentials = {
    "usernames": {
        "user1": {
            "name": "User One",
            "password": "password1"  # Replace with hashed password
        },
        "user2": {
            "name": "User Two",
            "password": "password2"  # Replace with hashed password
        },
    }
}

# Create authenticator
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="some_cookie_name",
    key="some_key",
    cookie_expiry_days=30,
)

# Login
name, authentication_status = authenticator.login("Login", "main")

if authentication_status:
    st.session_state["user_name"] = name  # Store username in session state
    st.success(f"Logged in as {name}!")
    st.experimental_rerun()  # Reload to main app

if authentication_status is False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password to access the app.")
