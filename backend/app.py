from api.youtube.stream import stream_format, create_stream
from googleapiclient.discovery import build
from flask import Flask, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
import datetime
import pathlib

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CLIENT_SECRETS_FILE = "credentials-youtube.json"

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    # Save creds in session or DB for future API calls
    session['credentials'] = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

    return 'Authentication successful! You can close this window.'

@app.route('/schedule_stream')
def schedule_stream_route():
    # Access credentials from session
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    creds_data = session['credentials']
    creds = Credentials(**creds_data)

    youtube = build('youtube', 'v3', credentials=creds)

    api_response = stream_format("I want to do a live steam of me playing rocket league. and if i lose a shave my head.")
    title = api_response['title']
    description = api_response['description']
    scheduled_time = datetime.datetime.fromisoformat("2025-07-25T18:00:00")

    create_stream(title, description, scheduled_time, youtube)

    return "Stream scheduled!"

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.run(port=8080)
