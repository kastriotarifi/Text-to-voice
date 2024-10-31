import streamlit as st
import pyttsx3
import tempfile

# Initialize TTS engine
engine = pyttsx3.init()

# Set voice options
voices = engine.getProperty('voices')
voice_options = { "Male": [voice for voice in voices if "male" in voice.name.lower()],
                  "Female": [voice for voice in voices if "female" in voice.name.lower()] }

# Streamlit app UI
def main():
    st.title("Text-to-Speech Converter")

    # Text input
    text = st.text_area("Enter text to convert to speech:")

    # Select voice gender and type
    gender = st.selectbox("Select Voice Gender", ["Male", "Female"])
    tone = st.selectbox("Select Voice Tone", ["Normal", "Deep", "Light"])

    # Set chosen voice
    selected_voice = voice_options.get(gender, [None])[0]
    if selected_voice:
        engine.setProperty('voice', selected_voice.id)

    # Adjust pitch or speed based on tone
    rate = engine.getProperty('rate')
    pitch_modifier = 0.9 if tone == "Deep" else 1.1 if tone == "Light" else 1.0
    engine.setProperty('rate', int(rate * pitch_modifier))

    if st.button("Convert and Preview Voice"):
        if text:
            # Generate and save audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                engine.save_to_file(text, temp_file.name)
                temp_file.seek(0)
                st.audio(temp_file.name, format="audio/mp3")

                # Download button
                st.download_button(
                    label="Download Audio",
                    data=temp_file.read(),
                    file_name="output.mp3",
                    mime="audio/mp3"
                )
        else:
            st.error("Please enter some text to convert.")

if __name__ == "__main__":
    main()
