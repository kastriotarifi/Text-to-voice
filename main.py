import os
import streamlit as st
from google.cloud import texttospeech
from google.oauth2 import service_account
import tempfile

# Authenticate to Google Cloud
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]  # Streamlit Cloud secrets
)
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Streamlit application
def main():
    st.title("Text-to-Speech with Gender and Voice Options")

    # Text input
    text = st.text_area("Enter text to convert to speech:", height=150)

    # Gender and voice options
    gender_options = {
        "Male - Deep": texttospeech.SsmlVoiceGender.MALE,
        "Male - Light": texttospeech.SsmlVoiceGender.MALE,
        "Female - Neutral": texttospeech.SsmlVoiceGender.FEMALE,
        "Female - High Pitch": texttospeech.SsmlVoiceGender.FEMALE
    }
    selected_gender = st.selectbox("Select Voice", options=list(gender_options.keys()))

    # Voice style options
    pitch = -2.0 if "Deep" in selected_gender else (2.0 if "High Pitch" in selected_gender else 0.0)

    if st.button("Convert and Preview"):
        if text:
            # Configure synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Configure voice parameters
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                ssml_gender=gender_options[selected_gender]
            )

            # Configure audio settings
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                pitch=pitch
            )

            # Perform TTS request
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            # Save audio to a temporary file for playback and download
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                temp_audio.write(response.audio_content)
                temp_audio_path = temp_audio.name

            # Audio playback and download button
            audio_file = open(temp_audio_path, "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            audio_file.close()

            # Download option
            with open(temp_audio_path, "rb") as f:
                st.download_button(
                    label="Download Audio",
                    data=f,
                    file_name="output.mp3",
                    mime="audio/mp3"
                )

            st.success("Audio generated and ready for download!")
            os.remove(temp_audio_path)
        else:
            st.error("Please enter some text to convert.")

if __name__ == '__main__':
    main()
