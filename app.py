import os
import streamlit as st
from modules.extract_audio import extract_audio
from modules.transcribe_audio import transcribe_audio
from modules.generate_srt import generate_srt
from modules.burn_caption import burn_subtitles

def main():
    st.title("AI-Powered Video Caption Generator")
    st.write("Upload video to generate captions")

    uploaded_video = st.file_uploader("Upload Video", type=["mp4", "mov"])
    if uploaded_video:
        video_path = "videos/uploaded_video.mp4"
        os.makedirs("videos", exist_ok=True)
        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())
        st.video(video_path)

        if st.button("Generate Captions"):
            os.makedirs("audio", exist_ok=True)
            audio_path = "audio/uploaded_audio.wav"
            st.write("Extracting audio...")
            if not extract_audio(video_path, audio_path):
                return

            st.write("Transcribing audio...")
            transcription_result = transcribe_audio(audio_path)
            if not transcription_result:
                return

            st.write("Transcription Result:")
            st.write(transcription_result.get("text", ""))

            st.write("Generating subtitles...")
            srt_content = generate_srt(transcription_result)
            os.makedirs("captions", exist_ok=True)
            srt_path = "captions/uploaded_output.srt"
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)
            st.success("SRT file generated")

            ffmpeg_path = "ffmpeg"
            st.write("Burning subtitles onto video...")
            if burn_subtitles(video_path, srt_path, "videos/uploaded_output_video.mp4", ffmpeg_path):
                st.success("Video with burned-in captions generated!")
                st.video("videos/uploaded_output_video.mp4")

if __name__ == "__main__":
    main()
