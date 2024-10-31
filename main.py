import streamlit as st
import pyttsx3
from io import BytesIO

# Initialize pyttsx3
engine = pyttsx3.init()

# Retrieve available voices
voices = engine.getProperty('voices')
voice_options = [("Male", voice) for voice in voices if "male" in voice.id.lower()] + \
                [("Female", voice) for voice in voices if "female" in voice.id.lower()]

def save_audio(engine, text, voice_id):
    """Save audio to a BytesIO buffer."""
    engine.setProperty('voice', voice_id)
    audio_buffer = BytesIO()
    engine.save_to_file(text, "output.mp3")
    engine.runAndWait()
    audio_buffer.seek(0)
    return audio_buffer

def main():
    st.title("Text-to-Speech Converter")

    # Text input
    text = st.text_area("Enter text to convert to speech:")

    # Select voice
    selected_voice = st.selectbox("Select Voice Type", voice_options, format_func=lambda x: x[0])

    # Generate voice when button is pressed
    if st.button("Generate Voice"):
        if text.strip():
            audio_buffer = save_audio(engine, text, selected_voice[1].id)
            st.audio(audio_buffer, format="audio/mp3")

            # Download button
            st.download_button(
                label="Download Audio",
                data=audio_buffer,
                file_name="output.mp3",
                mime="audio/mp3"
            )
        else:
            st.error("Please enter some text to convert.")

if __name__ == "__main__":
    main()
