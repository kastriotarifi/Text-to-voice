import streamlit as st
from gtts import gTTS
import time

# JavaScript code for local storage handling
local_storage_js = """
<script>
if (!localStorage.getItem('conversion_count')) {
    localStorage.setItem('conversion_count', '0');
}
if (!localStorage.getItem('last_reset')) {
    localStorage.setItem('last_reset', new Date().toISOString());
}

function resetConversionCountIfNewDay() {
    const lastReset = new Date(localStorage.getItem('last_reset'));
    const now = new Date();
    
    if (now.getDate() !== lastReset.getDate() || 
        now.getMonth() !== lastReset.getMonth() || 
        now.getFullYear() !== lastReset.getFullYear()) {
        localStorage.setItem('conversion_count', '0');
        localStorage.setItem('last_reset', now.toISOString());
    }
}

function getConversionCount() {
    return parseInt(localStorage.getItem('conversion_count'));
}

function incrementConversionCount() {
    let count = getConversionCount();
    count += 1;
    localStorage.setItem('conversion_count', count.toString());
}
resetConversionCountIfNewDay();
</script>
"""

# Streamlit application
def main():
    st.title("Text to Speech Converter")
    
    # Inject JavaScript into the Streamlit app
    st.components.v1.html(local_storage_js, height=0)

    # Display a link to click before proceeding
    if 'link_clicked' not in st.session_state:
        st.session_state.link_clicked = False

    if not st.session_state.link_clicked:
        st.write("Please visit this [link](https://example.com) to enable the converter.")
        if st.button("Click here to enable the converter"):
            st.session_state.link_clicked = True
            st.success("Converter enabled! You can now use it.")
    else:
        # Display remaining conversions
        current_count = st.session_state.get('conversion_count', 0)
        st.write(f"You have {10 - current_count} conversions left.")

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
                if current_count < 10:
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

                    # Increment conversion count in JavaScript
                    st.components.v1.html("<script>incrementConversionCount();</script>", height=0)
                    # Update session state count
                    st.session_state.conversion_count = current_count + 1
                else:
                    st.error("You have reached your daily limit of 10 conversions.")
            else:
                st.error("Please enter some text to convert.")

if __name__ == '__main__':
    main()
