import os
import streamlit as st
from modules.extract_audio import extract_audio
from modules.transcribe_audio import transcribe_audio
from modules.generate_srt import generate_srt
from modules.burn_caption import burn_subtitles

def main():
    st.set_page_config(page_title="AI Video Captioner", layout="centered")
    st.title("AI-Powered Video Caption Generator")
    st.write("Upload a video, and this tool will automatically generate and burn captions into it.")

    # Create directories if they don't exist
    os.makedirs("videos", exist_ok=True)
    os.makedirs("audio", exist_ok=True)
    os.makedirs("captions", exist_ok=True)

    uploaded_video = st.file_uploader("Upload a Video File", type=["mp4", "mov", "avi"])
    
    if uploaded_video:
        video_path = os.path.join("videos", "uploaded_video.mp4")
        
        # Save the uploaded video to the server
        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())
        
        st.video(video_path)

        if st.button("Generate Captions"):
            # Define paths for generated files
            audio_path = os.path.join("audio", "uploaded_audio.wav")
            srt_path = os.path.join("captions", "output.srt")
            output_video_path = os.path.join("videos", "output_video.mp4")

            with st.spinner("Step 1/4: Extracting audio from video..."):
                if not extract_audio(video_path, audio_path):
                    st.error("Could not extract audio. Please check the video file.")
                    return

            with st.spinner("Step 2/4: Transcribing audio to text... (This may take a moment)"):
                transcription_result = transcribe_audio(audio_path)
                if not transcription_result:
                    st.error("Audio transcription failed.")
                    return
            st.success("Audio transcribed successfully!")
            with st.expander("Show Full Transcription"):
                 st.write(transcription_result.get("text", "No text found."))


            with st.spinner("Step 3/4: Generating subtitle file (.srt)..."):
                srt_content = generate_srt(transcription_result)
                with open(srt_path, "w", encoding="utf-8") as f:
                    f.write(srt_content)
            st.success("SRT subtitle file generated!")

            with st.spinner("Step 4/4: Burning captions onto the video..."):
                if burn_subtitles(video_path, srt_path, output_video_path):
                    st.success("Video with burned-in captions is ready!")
                    st.video(output_video_path)
                    
                    with open(output_video_path, "rb") as file:
                        st.download_button(
                            label="Download Captioned Video",
                            data=file,
                            file_name="video_with_captions.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("Failed to burn subtitles into the video.")

if __name__ == "__main__":
    main()