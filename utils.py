import http.client
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import markdown
import requests

YT_API_KEY = os.getenv('YT_API_KEY', '')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
TELEGRAM_BOT_API_KEY= os.getenv('TELEGRAM_BOT_API_KEY', '')

# import json
# def load_config(file_path):
#     with open(file_path, 'r') as f:
#         return json.load(f)


# def init():
#     config = load_config('config.json')
#     global YT_API_KEY, SENDGRID_API_KEY, GEMINI_API_KEY, TELEGRAM_BOT_API_KEY
#     YT_API_KEY = config['YT_API_KEY']
#     SENDGRID_API_KEY = config['SENDGRID_API_KEY']
#     GEMINI_API_KEY = config['GEMINI_API_KEY']
#     TELEGRAM_BOT_API_KEY = config['TELEGRAM_BOT_API_KEY']

def get_latest_video(channel_id):
    conn = http.client.HTTPSConnection("youtube.googleapis.com")
    payload = ''
    headers = {
    'Accept': 'application/json'
    }
    conn.request("GET", "/youtube/v3/channels?part=contentDetails&id="+channel_id+"&key="+YT_API_KEY, payload, headers)
    response = conn.getresponse()
    print(YT_API_KEY)
    print("connection respoonse code = ",response.status)
    if response.status == 200:
        channel_data = json.loads(response.read().decode('utf-8'))
        playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        print(playlist_id)
        # Get the most recent video from the uploads playlist
        conn2 = http.client.HTTPSConnection("youtube.googleapis.com")
        payload = ''
        headers = {
        'Accept': 'application/json'
        }
        conn2.request("GET", "/youtube/v3/playlistItems?part=snippet&playlistId="+playlist_id+"&maxResults=1&key="+YT_API_KEY, payload, headers)
        playlist_response = conn2.getresponse()
        
        if playlist_response.status == 200:
            playlist_data = json.loads(playlist_response.read().decode('utf-8'))
            video = playlist_data['items'][0]
            video_title = video['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}"
            print(video_title, '-----', video_url)
            return video_title, video_url
        else:
            return None, None
    else:
        return None, None


def get_summary_from_llm(tokenized_transcript):
    conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
    payload = json.dumps({
        "contents": [
            {
            "parts": [
                {
                "text": "summarize the following text \n"+ tokenized_transcript 
                }
            ]
            }
        ]
    })
    headers = {
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1beta/models/gemini-1.5-flash:generateContent?key="+GEMINI_API_KEY, payload, headers)
    res = conn.getresponse()
    data = res.read()
    summarized_text = data.decode("utf-8")
    print(f"summary generated ------------- {summarized_text}")
    return summarized_text


def send_email(email, video_title, video_url, summary, channel_name):
    summary_html = markdown.markdown(summary)
    
    message = Mail(
        from_email = 'akgcorporate@proton.me',
        to_emails = email,
        subject="Here's your YouTube summary from Crypto space",
        html_content=f"""
            <strong>Channel Name: {channel_name}</strong><br>
            <strong>Video Title: {video_title}</strong>
            <br><br>
            <strong>Summary: </strong> 
            {summary_html}
            <br><br>
            <a href="{video_url}">Watch the video</a>
            """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def get_transcript_from_video(video_url):
    # Extract video ID from the video link
    video_id = video_url.split('v=')[1]
    # Get the transcript for the video
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
    captions = youtube.captions().list(part='snippet', videoId=video_id).execute()
    caption = captions['items'][0]['id']
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

    transcript_text=""

    for transcript in transcript_list:
        transcript_text+=transcript['text']

    if transcript_text!="":
        # chunk_size = 500
        # for i in range(0, len(transcript_txt), chunk_size):
        #     print(transcript_txt[i:i+chunk_size])
        # print(transcript_txt)
        return transcript_text
    else:
        print("Transcript not found")
        return None
    

def send_message_to_telegram(video_title, video_url, summary, channel_name):
    # Formatting TooooooooooDOooooo
    # summary_html = markdown.markdown(summary)
    # formatted_message = f"""
    #         # Here's your YouTube summary from Crypto space<br><br>
    #         <strong>Channel Name: {channel_name}</strong><br>
    #         <strong>Video Title: {video_title}</strong>
    #         <br><br>
    #         <strong>Summary: </strong> 
    #         {summary_html}
    #         <br><br>
    #         <a href="{video_url}">Watch the video</a>
    #         """
    video_metadata = f"Channel Name: {channel_name}\nVideo Title: {video_title}\nVideo URL: {video_url}\nSummary is as follows:"
    
    chat_id="@testingcryptoakg"
    url_video_metadata = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage?chat_id={chat_id}&text={video_metadata}&parse_mode=Markdown"
    requests.get(url_video_metadata)

    url_summary = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage?chat_id={chat_id}&text={summary}&parse_mode=Markdown"
    requests.get(url_summary)