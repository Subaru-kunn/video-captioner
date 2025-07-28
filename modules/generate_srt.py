import srt
from datetime import timedelta
import streamlit as st

def generate_srt(transcription_result):
    try:
        subtitles = []
        for i, seg in enumerate(transcription_result.get('segments', [])):
            subtitle = srt.Subtitle(
                index=i + 1,
                start=timedelta(seconds=seg['start']),
                end=timedelta(seconds=seg['end']),
                content=seg['text'].strip()
            )
            subtitles.append(subtitle)
        return srt.compose(subtitles)
    except Exception as e:
        st.error(f"Error generating SRT: {e}")
        return ""
