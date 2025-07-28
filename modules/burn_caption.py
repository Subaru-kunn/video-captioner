import ffmpeg
import streamlit as st
import os

def burn_subtitles(video_path, srt_path, output_path):
    """
    Burns subtitles into a video using ffmpeg-python.

    Args:
        video_path (str): The path to the input video file.
        srt_path (str): The path to the SRT subtitle file.
        output_path (str): The path to save the output video with subtitles.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Get absolute paths to ensure ffmpeg can find the files
        video_full = os.path.abspath(video_path)
        srt_full = os.path.abspath(srt_path)
        output_full = os.path.abspath(output_path)

        # Define the input video stream
        input_video = ffmpeg.input(video_full)
        
        # Use the 'subtitles' video filter to add the SRT file
        processed_video = ffmpeg.filter(input_video, 'subtitles', srt_full)

        # Define the output stream and execute the command
        # overwrite_output=True allows overwriting the file if it exists
        stream = ffmpeg.output(processed_video, output_full)
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        
        return True
    except ffmpeg.Error as e:
        # If an ffmpeg-specific error occurs, show the detailed error from ffmpeg
        st.error(f"Error burning subtitles with ffmpeg: {e.stderr.decode('utf8')}")
        return False
    except Exception as e:
        # Catch any other unexpected errors
        st.error(f"An unexpected error occurred during subtitle burning: {e}")
        return False