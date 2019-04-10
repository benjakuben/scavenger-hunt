import random

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

from scavenger.db import get_db, query_db

bp = Blueprint('sender', __name__, url_prefix='/sender')

current_item = None

@bp.route('/send', methods=['GET'])
def send_next_item():
    # Get a random item to scavenge
    # TODO: Track items used in a day
    items = query_db('SELECT name FROM items')
    current_item = items[random.randint(0, len(items))][0]
    message = f'Your next item to scavenge is: {current_item}'

    # Get all user numbers and send them the new item
    phone_numbers = query_db('SELECT phone_number FROM users')    
    for number in phone_numbers:
        # Send the message!
        send_sms(number[0], message)

    return(f'This page is for testing. Item sent: {current_item}')


def send_sms(phone_number, message):
    # Your Account SID from twilio.com/console
    account_sid = "ACc9f98fa556cecc1698e648d17f7b3f13"
    # Your Auth Token from twilio.com/console
    auth_token  = "429c4a11e7a4e3d271065852b63062e2"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=phone_number,
        from_="+14402765499",
        body=message
    )

    print(message.sid)