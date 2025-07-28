import whisper
import streamlit as st

def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return None
