import streamlit as st
from gtts import gTTS
from datetime import datetime

# JavaScript code to get and set local storage
get_local_storage = """
<script>
function getConversionCount() {
    return localStorage.getItem('conversion_count') || '0';
}
function setConversionCount(count) {
    localStorage.setItem('conversion_count', count);
}
function resetConversionCount() {
    localStorage.setItem('conversion_count', '0');
}
</script>
"""

# Function to reset count if it's a new day
def reset_count_if_new_day():
    last_reset = st.session_state.get('last_reset', None)
    if last_reset is None or (datetime.now() - last_reset).days > 0:
        st.session_state.conversion_count = 0
        st.session_state.last_reset = datetime.now()
        st.components.v1.html("<script>resetConversionCount();</script>", height=0)

# Function to get the conversion count from local storage
def get_conversion_count():
    count = st.session_state.get('conversion_count', 0)
    return int(count)

# Streamlit application
def main():
    st.title("Text to Speech Converter")
    
    # Insert JS code
    st.components.v1.html(get_local_storage, height=0)

    reset_count_if_new_day()

    # Get current conversion count from local storage
    current_count = get_conversion_count()
    st.session_state.conversion_count = current_count

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
                # Update local storage
                st.components.v1.html(f"<script>setConversionCount({st.session_state.conversion_count});</script>", height=0)
            else:
                st.error("You have reached your daily limit of 3 conversions.")
        else:
            st.error("Please enter some text to convert.")

if __name__ == '__main__':
    main()
