import io
import os

from urllib.request import urlopen, Request
from flask import Flask, request, redirect, Response
from twilio.twiml.messaging_response import MessagingResponse

# Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

"""
TODO: 
- scavenger hunt
    - send texts at random times, check results. Schedule the next one
    - Allow people to request another
    - Leaderboard?
"""

app = Flask(__name__)

def classify_image(image_url):
    # Instantiate a Google Vision client
    client = vision.ImageAnnotatorClient()

    # Get the image from the URL
    # Impersonate User-Agent to get around 403 error for urlopen
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    request = Request(url=image_url, headers=headers)
    content = urlopen(request).read()

    # Create a new image in memory
    image = types.Image(content=content)

    # Perform label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Output to console for testing
    for label in labels:
        print(f'{label.description}({label.score})\n')

    # Make sure we have labels returned
    if len(labels) > 0:
        label = labels[0].description
    else:
        label = 'Sorry, there was an error classifying your photo.'

    return label

@app.route('/submit', methods=['POST'])
def process_sms():
    # Get any media files (we're expecting 1 image)
    num_media = int(request.form.get('NumMedia', 0))
    media_files = [(request.form.get("MediaUrl{}".format(i), ''),
                    request.form.get("MediaContentType{}".format(i), ''))
                   for i in range(0, num_media)]
    
    # Check for image
    if num_media == 0:
        # TODO: Message about sending a photo
        reply = 'You must send a photo to play!'
    else:
        # Parse image
        if num_media > 1:
            # TODO: Add a message about just using the first image
            print('Please only send one image. We will only accept the first image in the group.')
        label = classify_image(media_files[0][0])
        reply = f'That looks like: {label}'

    response = MessagingResponse()
    response.message(reply)
    
    return str(response)

@app.route('/')
def build_index():
    return 'SMS Scavenger Hunt is up and running'

if __name__ == "__main__":
    app.run(debug=True)