import streamlit as st
import streamlit_authenticator as stauth
n 
# Users' data (this can be loaded from a file or database)
users = {
    "user1": {"name": "User One", "password": "password1"},
    "user2": {"name": "User Two", "password": "password2"},
}

# Create authenticator
authenticator = stauth.Authenticate(
    usernames=list(users.keys()),
    names=[user["name"] for user in users.values()],
    passwords=[user["password"] for user in users.values()],
    cookie_name="auth_cookie",
    key="auth",
    expiration_days=30,
)

# Login
name, authentication_status = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}!")
    st.session_state["user_name"] = name  # Store user name in session state
    st.session_state["login_page"] = False  # Switch to main page
    st.experimental_rerun()  # Reload to main
elif authentication_status is False:
    st.error("Username/password is incorrect.")
