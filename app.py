from moviepy.editor import VideoFileClip
import whisper
import srt
from datetime import timedelta
import subprocess
import os
import streamlit as st

# Step 1 : Extracting audio
def extract_audio(video_path, audio_output__path):
    try:
        video = VideoFileClip(video_path)
        if video.audio:
            video.audio.write_audiofile(audio_output__path)
            return True
        else:
            st.error("No audio track found in the video.")
            return False
    except Exception as e:
        st.error(f"Error extracting audio: {e}")
        return False
    
# Step 2 : Transcription
def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return None

# Step 3 : Generate SRT File
def generate_srt(transcription_result):
    try:
        subtitles = []
        for i, seg in enumerate(transcription_result.get('segments',[])):
            subtitle = srt.Subtitle(
                index = i+1,
                start=timedelta(seconds=seg['start']),
                end=timedelta(seconds=seg['end']),
                content=seg['text'].strip()
            )
            subtitles.append(subtitle)
        return srt.compose(subtitles)
    except Exception as e:
        st.error(f"Error generating SRT: {e}")
        return ""
    
# Step 4 : Buring subtitles using ffmpeg
def burn_subtitles(video_path, srt_relative_path, output_path, ffmpeg_path):
    video_full = os.path.abspath(video_path)
    output_full = os.path.abspath(output_path)

    command = f'"{ffmpeg_path}" -y -i "{video_full}" -vf "subtitles={srt_relative_path}" "{output_full}"'
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Error burning subtitles: {e}")
        return False

# Main Streamlit App
def main():
    st.title("AI-Powered Video Caption Generator")
    st.write("Upload a video to generate and burn captions onto it.")

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
            # st.write("Transcription Result :")
            # st.write(transcription_result.get("text", ""))

            srt_content = generate_srt(transcription_result)
            os.makedirs("captions", exist_ok=True)
            srt_path = "captions/uploaded_output.srt"
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)
            st.success("SRT file generated.")

            ffmpeg_path = r"C:\Users\The Chosen One\Downloads\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"
            st.write("Burning subtitles onto video...")
            if burn_subtitles(video_path, srt_path, "videos/uploaded_output_video.mp4", ffmpeg_path):
                st.success("video with burned-in captions generated!")
                st.video("videos/uploaded_output_video.mp4")


if __name__=="__main__":
    main()