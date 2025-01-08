# import http.client
# import json
# conn = http.client.HTTPSConnection("youtube.googleapis.com")
# payload = ''
# headers = {
#   'Accept': 'application/json'
# }

# conn.request("GET", "/youtube/v3/channels?part=contentDetails&id=UCrC8mOqJQpoB7NuIMKIS6rQ&key="+API_KEY, 
#              payload, headers)


# res = conn.getresponse()
# print(res.read().decode('utf-8'))
# channel_data = json.loads(res.read().decode('utf-8'))
# print(channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads'])

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from memory_profiler import profile


@profile
def send_email():
    message = Mail(
    from_email='akgcorporate@proton.me',
    to_emails='avdhesh.kumar1221@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
        
# send_email()

from vertexai.preview import tokenization

model_name = "gemini-1.5-flash-001"
tokenizer = tokenization.get_tokenizer_for_model(model_name)

contents = "summarize the following text \n I randomly started getting like moneydropped in my wallet and I didn't knowwhat it was from I've been playingaround with virtuals protocol I've beenplaying around with a bunch of differentAI Platforms in Defi and at first I waskind of like dude it's like 10 bucksfive bucks 20 bucks but then I startedgetting some that were like 200 bucks300 bucks 400 bucks 500 bucks and I waslike man this is kind of cool where isthis coming from and then I realized itwas coming from the different platformsthat I'm playing with"
result = tokenizer.count_tokens(contents)
print(f"Total tokens: {result.total_tokens}")