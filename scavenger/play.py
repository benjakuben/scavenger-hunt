
import functools
import io
import os

from scavenger.db import get_db, query_db
from scavenger.item import Item

from urllib.request import urlopen, Request
from twilio.twiml.messaging_response import MessagingResponse
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

# Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

bp = Blueprint('play', __name__, url_prefix='/play')

@bp.route('/submit', methods=['POST'])
def process_photo():
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
    
        reply = ''

        # Check for image
        if num_media == 0:
            reply = 'You must send a photo to play!'
        else:
            # Parse image
            if num_media > 1:
                print('Please only send one image. We will only accept the first image in the group.')
            labels = classify_image(media_files[0][0])

            if len(labels) == 0:
                reply = 'Not a match. Try another photo!'
            else: 
                for label in labels:
                    item = get_current_item()
                    if label.upper() == item.name.upper():
                        print('It\'s a match!')
                        # It's a match! Award points if not already matched for this user
                        points = 10
                        db.execute(
                            'INSERT INTO submissions (user_id, item_id, points) ' \
                            'VALUES (?, ?, ?)', 
                            (phone_number, item.id, points,)
                        )
                        db.commit()
                        reply = f'Nicely done! {points} points!'
                        break
                    else:
                        print(f'Not a match ({label}).')
                        reply = 'Not a match. Try another photo!'

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

    # Return a list of labels above the threshold
    top_labels = []
    for label in labels:
        print(f'{label.description}, {label.score}')
        if label.score > 0.6:
            top_labels.append(label.description)

    return top_labels


@bp.route('/players', methods=['GET'])
def list_players():
    players = query_db('SELECT * FROM users')
    return render_template('players.html', data=players)


@bp.route('/leaders', methods=['GET', 'POST'])
def show_leaderboard():
    leaders = get_leaders()
    if request.method == 'POST':
        leader_reply = ''
        for leader in leaders:
            leader_reply += f'{leader[0]}: {leader[1]} points\n'

        response = MessagingResponse()
        response.message(leader_reply)
        return str(response)
    else:
        return render_template('leaderboard.html', data=leaders)


def get_current_item():
    item = query_db(
        'SELECT r.item_id, i.name ' \
        'FROM rounds r ' \
        'JOIN items i ON i.id = r.item_id ' \
        'WHERE r.created = (SELECT MAX(created) FROM rounds)'
    )

    return Item(item[0][0], item[0][1])


def get_leaders():
    leaders = query_db(
        'SELECT user_id, SUM(points) FROM submissions GROUP BY user_id ORDER BY SUM(POINTS)'
    )
    return leaders