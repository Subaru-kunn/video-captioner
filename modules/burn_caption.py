import os
import subprocess
import streamlit as st

def burn_subtitles(video_path, srt_relative_path, output_path, ffmpeg_path):
    video_full = os.path.abspath(video_path)
    output_full = os.path.abspath(output_path)

    command = f'"{ffmpeg_path}" -i "{video_full}" -vf "subtitles={srt_relative_path}" "{output_full}"'

    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Error burning subtitles: {e}")
        return False
