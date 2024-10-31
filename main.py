import streamlit as st
import streamlit_authenticator as stauth
from gtts import gTTS

# Define credentials with hashed passwords
credentials = {
    "usernames": ["user1", "user2"],
    "names": ["User One", "User Two"],
    "passwords": ["password1", "password2"]
}

# Create authenticator
authenticator = stauth.Authenticate(
    credentials["usernames"],
    credentials["names"],
    credentials["passwords"],
    cookie_name="some_cookie_name",
    key="some_key",
    cookie_expiry_days=30,
)

# Login
name, authentication_status = authenticator.login("Login", "main")

if authentication_status:
    st.title("Text to Speech Converter")

    # Text input
    text = st.text_area("Enter text to convert to speech:", height=150)

    # Language options for voice selection
    language_options = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Chinese": "zh",
    }
    selected_language = st.selectbox("Select Language", options=list(language_options.keys()))

    if st.button("Convert to Voice"):
        if text:
            # Initialize gTTS object with the input text and selected language
            tts = gTTS(text=text, lang=language_options[selected_language], slow=False)

            # Save the audio file
            audio_file = "output.mp3"
            tts.save(audio_file)

            # Provide download link
            with open(audio_file, "rb") as f:
                st.download_button(
                    label="Download Audio",
                    data=f,
                    file_name="output.mp3",
                    mime="audio/mp3"
                )
            st.success("Voice generated and saved successfully!")
        else:
            st.error("Please enter some text to convert.")
else:
    st.warning("Please enter your username and password to access the app.")
