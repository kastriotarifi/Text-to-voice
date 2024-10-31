import streamlit as st
from gtts import gTTS

# Streamlit application
def main():
    st.title("Text to Speech Converter")

    # Converter logic
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

    # Button to display an ad
    if st.button("Display Ad"):
        st.markdown("[Click here for the ad!](https://example.com)")  # Change to your desired URL

if __name__ == '__main__':
    main()
