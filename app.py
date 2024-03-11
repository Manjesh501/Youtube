import streamlit as st
from dotenv import load_dotenv
load_dotenv()# load all env variable
import os
from youtube_transcript_api import YouTubeTranscriptApi



import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt ="""
Generate detailed notes from a YouTube video Recognize different languages and accents. 
Understand the context of the video content, including technical terms and domain-specific language. 
Utilize natural language processing techniques to analyze and summarize the content effectively. 
 Provide summarized notes in short and also provide  detailed notes with complete information , you can use any style or way for notes . 
."""

##we have to get transcript from youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id= youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for i in transcript_text:
            transcript = transcript +i['text'] # we hqave got transcript in the form of list we are converting it in para
        return transcript
    except Exception as e:
        raise e
    
#getting summary based on propmpt using Gemini pro
def generate_gemini_content(transcript_text,prompt):
    model= genai.GenerativeModel("gemini-pro")
    response= model.generate_content(prompt + transcript_text)
    return response.text

##looks
st.title("Youtube video to detailed notes converter ")
youtube_link= st.text_input("Enter Youtuve video link: ")

if youtube_link:
    video_id= youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width= True)

if st.button("Get detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("Here is Your detailed notes ")
        st.write(summary)

