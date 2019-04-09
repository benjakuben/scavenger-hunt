
import functools

from twilio.twiml.messaging_response import MessagingResponse
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

from scavenger.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/join', methods=['GET'])
def process_sms():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        print(phone_number)
        db = get_db()
        error = None

        print('1')
        if not phone_number:
            print('2')
            error = 'Error getting user\'s phone number.'
        elif db.execute(
            'SELECT phone_number FROM users WHERE phone_number = ?', (phone_number,)
        ).fetchone() is not None:
            error = '{} is already registered.'.format(phone_number)

        print('3')
        if error is None:
            db.execute(
                'INSERT INTO users (phone_number) VALUES (?)', (phone_number)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        print('4')
        flash(error)

        print('5')
        response = MessagingResponse()
        response.message('Success! We\'ll message you when the next round starts!')
        return str(response)

    elif request.method == 'GET':
        # return render_template('auth/register.html')
        return('To join the hunt, text \'JOIN\' to 440-276-5499!')


    # Get any media files (we're expecting 1 image)
    # num_media = int(request.form.get('NumMedia', 0))
    # media_files = [(request.form.get("MediaUrl{}".format(i), ''),
    #                 request.form.get("MediaContentType{}".format(i), ''))
    #                for i in range(0, num_media)]
    
    # # Check for image
    # if num_media == 0:
    #     # TODO: Message about sending a photo
    #     reply = 'You must send a photo to play!'
    # else:
    #     # Parse image
    #     if num_media > 1:
    #         # TODO: Add a message about just using the first image
    #         print('Please only send one image. We will only accept the first image in the group.')
    #     label = classify_image(media_files[0][0])
    #     reply = f'That looks like: {label}'
