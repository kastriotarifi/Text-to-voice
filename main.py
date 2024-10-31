import streamlit as st
from gtts import gTTS
from datetime import datetime, timedelta

# Initialize session state
if 'conversion_count' not in st.session_state:
    st.session_state.conversion_count = 0
if 'last_reset' not in st.session_state:
    st.session_state.last_reset = datetime.now()

# Function to reset the conversion count
def reset_conversion_count():
    if datetime.now() - st.session_state.last_reset >= timedelta(days=1):
        st.session_state.conversion_count = 0
        st.session_state.last_reset = datetime.now()

# Streamlit application
def main():
    st.title("Text to Speech Converter")
    reset_conversion_count()

    # Show remaining conversions
    st.write(f"You have {3 - st.session_state.conversion_count} conversions left today.")

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
            if st.session_state.conversion_count < 3:
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

                # Increment conversion count
                st.session_state.conversion_count += 1
            else:
                st.error("You have reached your daily limit of 3 conversions.")
        else:
            st.error("Please enter some text to convert.")

if __name__ == '__main__':
    main()
