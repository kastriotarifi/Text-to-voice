import streamlit as st
from gtts import gTTS
import time

# Streamlit application
def main():
    st.title("Text to Speech Converter")

    # Check if the user has clicked the link
    if 'link_clicked' not in st.session_state:
        st.session_state.link_clicked = False

    # Show the link and button if the link hasn't been clicked
    if not st.session_state.link_clicked:
        if st.button("Open Website"):
            # Simulate opening a website
            st.session_state.link_clicked = True
            st.success("You have clicked the link! You can now use the converter.")
            st.markdown("[Click here to visit the website](https://example.com)")  # Change to your desired URL
            time.sleep(2)  # Optional delay

    # Converter logic
    if st.session_state.link_clicked:
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

                # Audio preview
                audio_preview = open(audio_file, "rb").read()
                st.audio(audio_preview, format="audio/mp3")

                # Download link
                st.download_button(
                    label="Download Audio",
                    data=audio_preview,
                    file_name="output.mp3",
                    mime="audio/mp3"
                )
                st.success("Voice generated and available for download and preview.")
            else:
                st.error("Please enter some text to convert.")

if __name__ == '__main__':
    main()
