import os
from moviepy.editor import VideoFileClip
import streamlit as st

def extract_audio(video_path, audio_output_path):
    try:
        video = VideoFileClip(video_path)
        if video.audio:
            video.audio.write_audiofile(audio_output_path)
            return True
        else:
            st.error("No audio track found in the video")
            return False
    except Exception as e:
        st.error(f"Error extracting audio: {e}")
        return False
