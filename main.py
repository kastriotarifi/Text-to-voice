import streamlit as st
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# Streamlit application
def main():
    st.title("Text to Speech Converter")

    # Text input
    text = st.text_area("Enter text to convert to speech:", height=150)

    # Dropdown to select voice
    voice_options = {f"{voice.name} ({voice.languages})": voice.id for voice in voices}
    selected_voice = st.selectbox("Select Voice", options=list(voice_options.keys()))

    # Dropdown to select language
    language_options = {
        "English (US)": "en_US",
        "English (UK)": "en_GB",
        "Spanish": "es_ES",
        "French": "fr_FR",
        "German": "de_DE",
        "Italian": "it_IT",
        "Chinese (Mandarin)": "zh_CN",
    }
    selected_language = st.selectbox("Select Language", options=list(language_options.keys()))

    if st.button("Convert to Voice"):
        if text:
            # Set the selected voice
            engine.setProperty('voice', voice_options[selected_voice])

            # Set speech rate (optional)
            rate = engine.getProperty('rate')   # Get current rate
            engine.setProperty('rate', rate - 50)  # Decrease rate for better clarity

            # Save the audio file
            filename = "output.mp3"
            engine.save_to_file(text, filename)
            engine.runAndWait()

            # Provide download link
            with open(filename, "rb") as f:
                st.download_button(
                    label="Download Audio",
                    data=f,
                    file_name="output.mp3",
                    mime="audio/mp3"
                )
            st.success("Voice generated and saved successfully!")
        else:
            st.error("Please enter some text to convert.")

if __name__ == '__main__':
    main()
