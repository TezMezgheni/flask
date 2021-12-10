import youtube_transcript_api

from Summarize import summarize
from app import *

video_link = input("give youtube link ")
video_id = get_yt_video_id(video_link)
transcript = Transcript.transcript_parser(video_id)
print(summarize(transcript))
