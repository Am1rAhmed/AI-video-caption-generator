# AI-video-caption-generator
AI-Powered Video Caption Generator is a Streamlit-based web application that automatically generates subtitles for videos using OpenAI Whisper. It extracts audio, transcribes speech with high accuracy, generates SRT subtitle files, and embeds captions directly into videos using FFmpeg — delivering fast, automated, and accessible video captioning.

Features:
Upload videos in MP4/MOV formats
Automatic audio extraction
High-accuracy speech-to-text transcription using Whisper
Auto-generation of SRT subtitle files
Burn captions directly into videos using FFmpeg
Download and preview captioned videos
Simple, interactive Streamlit web interface

Tech Stack:
Programming Language -	Python
Frontend	- Streamlit
Speech Recognition	- OpenAI Whisper
Video Processing -	MoviePy
Subtitle Generation - srt
Video Rendering	- FFmpeg

How It Works:
Upload a video
Audio is extracted using MoviePy
Whisper transcribes speech into text
Subtitles are converted to .srt
FFmpeg embeds subtitles into the video
Final captioned video is generated

