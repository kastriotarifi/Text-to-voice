import streamlit as st
from gtts import gTTS
import tempfile
import os

# Streamlit application
def main():
    st.title("Advanced Text-to-Speech Converter")

    # Text input
    text = st.text_area("Enter text to convert to speech:", height=150)

    # Language and voice options
    language_options = {
        "English (US, Male)": ("en", "com"),
        "English (UK, Female)": ("en", "gb"),
        "French (Male)": ("fr", "fr"),
        "French (Female)": ("fr", "ca"),
        "Spanish (Male)": ("es", "es"),
        "Spanish (Female)": ("es", "mx"),
    }
    selected_voice = st.selectbox("Select Voice", options=list(language_options.keys()))

    # Voice style options (deep/light)
    voice_style = st.radio("Select Voice Style", options=["Normal", "Deep", "Light"])

    # Handle the TTS synthesis on button click
    if st.button("Convert and Preview"):
        if text:
            # Fetch selected language and accent
            lang_code, accent = language_options[selected_voice]
            slow_speed = voice_style == "Deep"
            fast_speed = voice_style == "Light"
            
            # Set speed for gTTS based on voice style
            tts = gTTS(text=text, lang=lang_code, slow=slow_speed)
            
            # Save to a temporary file to allow preview and download
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                audio_path = temp_audio.name
                tts.save(audio_path)
            
            # Play audio in Streamlit for preview
            audio_file = open(audio_path, "rb")
            st.audio(audio_file, format="audio/mp3")
            audio_file.close()

            # Provide download link
            with open(audio_path, "rb") as f:
                st.download_button(
                    label="Download Audio",
                    data=f,
                    file_name="output.mp3",
                    mime="audio/mp3"
                )
            st.success("Voice generated, previewed, and ready for download!")
            
            # Clean up temporary file after download
            os.remove(audio_path)
        else:
            st.error("Please enter some text to convert.")

if __name__ == '__main__':
    main()
