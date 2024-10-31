import streamlit as st
from gtts import gTTS
from io import BytesIO

def main():
    st.title("Text-to-Speech Converter")

    # Text input
    text = st.text_area("Enter text to convert to speech:")

    # Select voice characteristics
    gender = st.selectbox("Select Voice Type", ["Male", "Female"])
    tone = st.selectbox("Select Tone", ["Normal", "Deep", "Light"])

    # Generate voice when the button is pressed
    if st.button("Generate Voice"):
        if text.strip():
            # Generate TTS using gTTS
            tts = gTTS(text=text, lang="en")
            
            # Save TTS to an audio buffer
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            # Streamlit's audio player for preview
            st.audio(audio_buffer, format="audio/mp3")

            # Provide download link
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
