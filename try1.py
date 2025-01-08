import time
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from vertexai.preview import tokenization
from database import *
from utils import *

if __name__ == "__main__":
    init()

def get_summary_from_transcript(transcript):
    # 1. Get number of tokens the transcript
    model_name = "gemini-1.5-flash-001"
    tokenizer = tokenization.get_tokenizer_for_model(model_name)

    contents = transcript
    countTokensResult = tokenizer.count_tokens(contents)
    print(f"Total tokens : {countTokensResult.total_tokens}")
    # 2. check tokens allowed and pass it to the model. 
    # 3. get the summary from the model function. async await
    # Placeholder function to get summary from video URL call gemini API
    summary = get_summary_from_llm(transcript)
    return summary


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
        
 

def get_user_from_db(user_id):
    # Placeholder function to simulate fetching user from database
    # Replace this with actual database query logic
    map = {}
    map["akg"] = "avdhesh.kumar1221@gmail.com"
    map["kc"] = "kaishikchandra010@gmail.com"
    
    return map.get(user_id)
        

def send_notification(user_id, video_title, video_url, summary):
    email = get_user_from_db(user_id)
    if summary is not None:
        send_email(email, video_title, video_url, summary)
    else:
        print("Summary not found, skipping email notification.")
    



# import schedule
import time

def job():
    db_name = "channelsVideoData.db"
    subscribed_channels = list_channel_ids(db_name)
    # subscribed_channels = ["UCt7esZt_MwWXl9fgT0yO1eA", "UCbLhGKVY-bJPcawebgtNfbw"]
    for channel_id in subscribed_channels:
        video_title, video_url = get_latest_video(channel_id)
        
        if video_url:
            # Compare with stored video ID in the database
            data = read_channel("channelsVideoData.db",channel_id)
            all_videos_string = data['videos']
            # sample response ['Video3', 'Video4']
            if(all_videos_string == None):
                all_videos_string = ""
            if video_url not in all_videos_string:
                # Update the channel
                video = [video_url]
                update_channel(db_name, channel_id, video)
                print("New video, pushing to get summary.")
                transcript = get_transcript_from_video(video_url)
                print("got transcript.")
                summary = get_summary_from_transcript(transcript)
                print("got summary.")
                # ToDo: iterate for all the users
                print("TooooooooDooooooooo \n Sending notification to all users")
                send_notification("akg",video_title, video_url, summary)
                send_notification("kc",video_title, video_url, summary)
                # store_video_in_db(channel_id, video_url)
            else:
                print("Video already processed, skipping.")
                


# schedule.every(5).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

job()