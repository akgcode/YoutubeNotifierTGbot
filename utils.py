import http.client
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

YT_API_KEY = ''
SENDGRID_API_KEY = ''
GEMINI_API_KEY = ''

import json
def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def init():
    config = load_config('config.json')
    YT_API_KEY = config['YT_API_KEY']
    SENDGRID_API_KEY = config['SENDGRID_API_KEY']
    GEMINI_API_KEY = config['GEMINI_API_KEY']
    print(YT_API_KEY, SENDGRID_API_KEY, GEMINI_API_KEY)

init()

def get_latest_video(channel_id):
    conn = http.client.HTTPSConnection("youtube.googleapis.com")
    payload = ''
    headers = {
    'Accept': 'application/json'
    }
    conn.request("GET", "/youtube/v3/channels?part=contentDetails&id="+channel_id+"&key="+YT_API_KEY, payload, headers)
    response = conn.getresponse()

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


def send_email(email, video_title, video_url, summary):
    message = Mail(
        from_email = 'akgcorporate@proton.me',
        to_emails = email,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=f"""
            <strong>{video_title}</strong>
            <br><br>
            Summary: {summary}
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

