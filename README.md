# Scavenger Hunt

An SMS-based scavenger hunt where players are sent a text of an object they need to find, photograph, and send back in a reply. Photos are analyzed using Google's Vision API, which determines if the photo counts as a match for the challenge.

Check it out at [https://b2fda460.ngrok.io](https://b2fda460.ngrok.io)!

# Running this app

Follow the instructions below to install requirements and run this app for this interview exercise.

## Installation
If Flask and other libraries are needed: 
```
pip install -r requirements.txt
```

## Google Vision API
```
export GOOGLE_APPLICATION_CREDENTIALS=<path to .json key> # from Google Cloud console
```

## Running the app
Set up your local Flask environment:
```
export FLASK_APP=scavenger
export FLASK_ENV=development
flask run
```