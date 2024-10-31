import streamlit as st
from gtts import gTTS
import os

# Streamlit application
def main():
    st.title("Text to Speech Converter")

    # Get text input from the user
    text = st.text_area("Enter the text you want to convert to speech:", height=150)

    if st.button("Convert to Voice"):
        # Check if text is not empty
        if not text.strip():
            st.error("No text provided. Please enter some text.")
            return

        # Initialize gTTS object with the input text
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save the audio file
        filename = "output.mp3"
        tts.save(filename)
        
        # Provide download link
        with open(filename, "rb") as audio_file:
            st.audio(audio_file, format="audio/mp3")
            st.success("Voice generated successfully!")

        # Optionally, you can also provide a download button for the audio file
        st.download_button(
            label="Download Audio",
            data=open(filename, "rb").read(),
            file_name="output.mp3",
            mime="audio/mp3"
        )

if __name__ == '__main__':
    main()
