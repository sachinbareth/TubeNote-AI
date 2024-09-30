import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for summarization
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 400 words. Please provide the summary of the text given here:  """


# Function to extract video ID from various YouTube URL formats
def extract_video_id(youtube_video_url):
    match = re.search(r'(?:youtu\.be/|(?:www\.)?youtube\.com/(?:[^/]+/.*|(?:v|e(?:mbed)?)|.*[?&]v=))([^&]{11})', youtube_video_url)
    return match.group(1) if match else None


# Function to get the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    video_id = extract_video_id(youtube_video_url)
    if not video_id:
        return "Invalid YouTube URL. Please provide a valid link."

    try:
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine transcript parts into a single string
        transcript = " ".join([i["text"] for i in transcript_text])

        return transcript

    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Function to get the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# Streamlit UI
st.title("TubeNote AI")
youtube_link = st.text_input("Paste the YouTube video URL, and let the AI summarize it for you!")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Extract the Key Points"):
    transcript_text = extract_transcript_details(youtube_link)

    if "Invalid YouTube URL" in transcript_text or "Transcripts are disabled" in transcript_text:
        st.warning(transcript_text)
    else:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Essential Points:")
        st.write(summary)
