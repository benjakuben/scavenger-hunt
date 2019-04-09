
import functools

from twilio.twiml.messaging_response import MessagingResponse
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

from scavenger.db import get_db, query_db

bp = Blueprint('play', __name__, url_prefix='/play')

@bp.route('/submit', methods=['POST'])
def process_sms():
    phone_number = request.form['From']
    db = get_db()
    error = None

    if not phone_number:
        error = 'Error getting user\'s phone number.'
    elif db.execute(
        'SELECT phone_number FROM users WHERE phone_number = ?', (phone_number,)
    ).fetchone() is not None:
        # Get any media files (we're expecting 1 image)
        num_media = int(request.form.get('NumMedia', 0))
        media_files = [(request.form.get("MediaUrl{}".format(i), ''),
                        request.form.get("MediaContentType{}".format(i), ''))
                       for i in range(0, num_media)]
    
        # Check for image
        if num_media == 0:
            reply = 'You must send a photo to play!'
        else:
            # Parse image
            if num_media > 1:
                print('Please only send one image. We will only accept the first image in the group.')
            label = classify_image(media_files[0][0])
            reply = f'That looks like: {label}'

    # if error is None:
    #     db.execute(
    #         'INSERT INTO users (phone_number) VALUES (?)', (phone_number,)
    #     )
    #     db.commit()
    #     return redirect(url_for('auth.process_sms'))

    # flash(error)

    response = MessagingResponse()
    response.message(reply)
    
    return str(response)


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


@bp.route('/players', methods=['GET'])
def list_players():
    players = query_db('SELECT * FROM users')
        # print(f"Phone #: {user['phone_number']}, id: {user['id']}")
    return render_template('players.html', data=players)

