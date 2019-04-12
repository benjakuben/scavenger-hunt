import functools

from twilio.twiml.messaging_response import MessagingResponse
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

from scavenger.db import get_db, query_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

WELCOME_MESSAGE = 'Welcome to the hunt! We\'ll message you when the next round starts. ' \
    'Text \'q\' to quit or \'leaders\' for today\'s leaderboard. Send a picture (no text) ' \
    'when you find the latest item!'

@bp.route('/join', methods=['GET', 'POST'])
def process_join():
    if request.method == 'POST':
        phone_number = request.form['From']
        db = get_db()
        error = None

        if not phone_number:
            error = 'Error getting user\'s phone number.'
        elif db.execute(
            'SELECT phone_number FROM users WHERE phone_number = ?', (phone_number,)
        ).fetchone() is not None:
            error = '{} is already registered.'.format(phone_number)

        if error is None:
            db.execute(
                'INSERT INTO users (phone_number) VALUES (?)', (phone_number,)
            )
            db.commit()
            return redirect(url_for('auth.process_join'))

        flash(error)

        response = MessagingResponse()
        response.message(WELCOME_MESSAGE)
        return str(response)

    elif request.method == 'GET':
        return('To join the hunt, text \'JOIN\' to 440-276-5499!')


@bp.route('/quit', methods=['POST'])
def process_quit():
    phone_number = request.form['From']
    db = get_db()
    error = None

    if not phone_number:
        error = 'Error getting user\'s phone number.'
    else:
        db.execute(
            'DELETE FROM users WHERE phone_number = ?', (phone_number,)
        )
        db.commit()

    response = MessagingResponse()
    response.message('You have left the game. Text \'join\' to start again!')
    return str(response)
