import os
import streamlit as st
from modules.extract_audio import extract_audio
from modules.transcribe_audio import transcribe_audio
from modules.generate_srt import generate_srt
from modules.burn_caption import burn_subtitles

st.set_page_config(
    page_title="Video Caption Generator",
    layout="centered",
    initial_sidebar_state="auto"
)

# CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #111827;
            color: white;
        }
        h1, h2, h3 {
            color: white;
        }
        .stButton>button {
            color: white;
            background-color: #2563eb;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #1e40af;
        }
        .uploadedFileName {
            text-align: center;
        }
        video {
            border: 2px solid #2563eb;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Main App
def main():
    st.markdown("<h1 style='text-align: center;'>🎥 AI-Powered Video Caption Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload a video and generate intelligent captions with a single click!</p>", unsafe_allow_html=True)

    uploaded_video = st.file_uploader("Upload Video", type=["mp4", "mov", "mpeg4"])

    if uploaded_video:
        video_path = "videos/uploaded_video.mp4"
        os.makedirs("videos", exist_ok=True)
        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        st.video(video_path)

        if st.button("Generate Captions"):
            os.makedirs("audio", exist_ok=True)
            audio_path = "audio/uploaded_audio.wav"
            st.info("🔊 Extracting audio...")
            if not extract_audio(video_path, audio_path):
                st.error("Failed to extract audio.")
                return

            st.info(" Transcribing audio...")
            transcription_result = transcribe_audio(audio_path)
            if not transcription_result:
                st.error("Failed to transcribe audio.")
                return

            st.subheader("Transcription Result")
            st.write(transcription_result.get("text", ""))

            st.info("Generating subtitles...")
            srt_content = generate_srt(transcription_result)

            os.makedirs("captions", exist_ok=True)
            srt_path = "captions/uploaded_output.srt"
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)

            ffmpeg_path = "ffmpeg" 
            st.info(" Burning subtitles onto video...")
            output_video_path = "videos/uploaded_output_video.mp4"
            if burn_subtitles(video_path, srt_path, output_video_path, ffmpeg_path):
                st.success(" Captioned video ready !!!")
                st.video(output_video_path)
            else:
                st.error("⚠️ Failed to burn subtitles onto video.")

if __name__ == "__main__":
    main()
