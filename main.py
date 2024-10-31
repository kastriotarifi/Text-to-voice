import streamlit as st
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Streamlit App
def main():
    st.title("Text-to-Speech Converter")

    # Text input
    text = st.text_area("Enter text to convert to speech:")

    # Select voice characteristics
    gender = st.selectbox("Select Voice Type", ["Male", "Female"])
    tone = st.selectbox("Select Tone", ["Normal", "Deep", "Light"])

    # Check if there's text to convert
    if st.button("Generate Voice"):
        if text.strip():
            # Generate TTS
            tts = gTTS(text=text, lang="en")

            # Save to a BytesIO buffer to preview
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            # Load audio and modify pitch if needed
            audio = AudioSegment.from_file(audio_buffer, format="mp3")
            if tone == "Deep":
                audio = audio.lower() + 4
            elif tone == "Light":
                audio = audio.speedup(1.1)

            # Save the modified audio for playback and download
            final_audio_buffer = BytesIO()
            audio.export(final_audio_buffer, format="mp3")
            final_audio_buffer.seek(0)

            # Preview the audio
            st.audio(final_audio_buffer, format="audio/mp3")

            # Download button
            st.download_button(
                label="Download Audio",
                data=final_audio_buffer,
                file_name="output.mp3",
                mime="audio/mp3"
            )
        else:
            st.error("Please enter some text to convert.")

if __name__ == "__main__":
    main()
