import os
import subprocess
import streamlit as st

def burn_subtitles(video_path, srt_path, output_path, ffmpeg_path="ffmpeg"):
    video_full = os.path.abspath(video_path)
    srt_full = os.path.abspath(srt_path)
    output_full = os.path.abspath(output_path)

    command = [
        ffmpeg_path,
        "-y", 
        "-i", video_full,
        "-vf", f"subtitles='{srt_full}'",
        output_full
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"FFmpeg Error: {e.stderr}")
        return False
