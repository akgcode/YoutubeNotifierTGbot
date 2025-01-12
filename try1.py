import time
import logging
from vertexai.preview import tokenization
from database import *
from utils import *
from memory_profiler import profile
import schedule

# if __name__ == "__main__":
#     init()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_summary_from_transcript(transcript):
    logging.info("Starting get_summary_from_transcript function")
    
    # 1. Get number of tokens the transcript
    model_name = "gemini-1.5-flash-001"
    tokenizer = tokenization.get_tokenizer_for_model(model_name)
    logging.info(f"Using model: {model_name}")

    contents = transcript
    countTokensResult = tokenizer.count_tokens(contents)
    logging.info(f"Total tokens: {countTokensResult.total_tokens}")
    
    # 2. check tokens allowed and pass it to the model. 
    # 3. get the summary from the model function. async await
    # Placeholder function to get summary from video URL call gemini API
    response = get_summary_from_llm(transcript)
    logging.info("Received response from LLM")
    
    summaryJson = json.loads(response)
    summary = summaryJson['candidates'][0]['content']['parts'][0]['text']
    logging.info(f"Extracted summary from response:{summary}")
    
    return summary




def get_user_from_db(user_id):
    # Placeholder function to simulate fetching user from database
    # Replace this with actual database query logic
    map = {}
    map["akg"] = "avdhesh.kumar1221@gmail.com"
    map["kc"] = "KaushikChandra010@gmail.com"
    
    return map.get(user_id)
        

def send_notification(user_id, video_title, video_url, summary, channel_name):
    email = get_user_from_db(user_id)
    if summary is not None:
        send_message_to_telegram(video_title, video_url, summary, channel_name)
        send_email(email, video_title, video_url, summary, channel_name)
    else:
        logging.error("Summary not found, skipping email notification.")
    

# @profile
def job():
    # init()
    logging.info("Job started")
    db_name = "channelsVideoData.db"
    subscribed_channels = list_channel_ids(db_name)
    # subscribed_channels = []
    logging.info(subscribed_channels)
    
    # subscribed_channels = ["UCt7esZt_MwWXl9fgT0yO1eA", "UCbLhGKVY-bJPcawebgtNfbw"]
    for channel_id in subscribed_channels:
        channel_name = read_channel("channelsVideoData.db",channel_id)['channel_name']
        video_title, video_url = get_latest_video(channel_id)
        logging.debug(video_title, video_url)
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
                logging.debug("New video, pushing to get summary.")
                transcript = get_transcript_from_video(video_url)
                logging.debug("got transcript.")
                summary = get_summary_from_transcript(transcript)
                logging.debug("got summary.")
                # ToDo: iterate for all the users
                logging.debug("Sending notification to all users")
                # send_notification("akg",video_title, video_url, summary, channel_name)
                send_notification("kc",video_title, video_url, summary, channel_name)
                # store_video_in_db(channel_id, video_url)
            else:
                print("Video already processed, skipping.")
        # add delay of 1 sec
        time.sleep(1)


