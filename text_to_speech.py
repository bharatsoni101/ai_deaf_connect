from gtts import gTTS
import streamlit as st
import tempfile
import os
import base64


def speak_text(text):
    """
    Convert text to speech and automatically play it.

    Input:
        text (str): Word or sentence to speak
    """

    # Ignore empty or invalid text
    if not text or text in ["UNRECOGNIZED", "No Hand Detected"]:
        return

    try:

        # Create a temporary MP3 file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        temp_path = temp_file.name
        temp_file.close()

        # Convert text to speech
        tts = gTTS(
            text=text,
            lang="en"
        )

        # Save MP3 file
        tts.save(temp_path)

        # Read MP3 bytes
        with open(temp_path, "rb") as audio_file:

            audio_bytes = audio_file.read()

        # Convert audio into Base64
        audio_base64 = base64.b64encode(
            audio_bytes
        ).decode()

        # HTML audio player with autoplay enabled
        audio_html = f"""
        <audio autoplay>
            <source
                src="data:audio/mp3;base64,{audio_base64}"
                type="audio/mp3">
        </audio>
        """

        # Hide player and play automatically
        st.markdown(
            audio_html,
            unsafe_allow_html=True
        )

        # Remove temporary file
        os.remove(temp_path)

    except Exception as e:

        st.error(
            f"Speech conversion error: {e}"
        )