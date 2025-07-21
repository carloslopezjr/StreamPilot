from api.youtube.stream import stream_format, create_stream
from api.leetcode.query_problems import fetch_leetcode_questions, load_approved_problems, fetch_all_approved_unique_problem_names
from googleapiclient.discovery import build
from flask import Flask, redirect, request, session, url_for, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
import datetime
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

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

@app.route('/schedule_stream', methods=['POST'])
def schedule_stream():
    # If not authenticated, return auth URL to frontend
    if 'credentials' not in session:
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
        # Return JSON to frontend to tell it to redirect user
        return jsonify({'auth_required': True, 'auth_url': authorization_url}), 401

    # If authenticated, proceed
    creds_data = session['credentials']
    creds = Credentials(**creds_data)
    youtube = build('youtube', 'v3', credentials=creds)

    data = request.get_json()
    prompt = data.get('input')
    difficulty = data.get("difficulty")
    difficulty = [item.upper() for item in difficulty]
    topics = data.get("topics")
    topics = [item.upper() for item in topics]
    date = data.get('date')
    time = data.get('time')
    hwg_cookies = "LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTI3ODIxNDkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5Mzc4MmNhYzAxYzVlMDI2ZDU4ZmUxZGJmZWQ1MDkzYmMxMWI3NjkzZGE4Zjg1MmM0ZGJiNjM0ZWVhMDZhZDhkIiwic2Vzc2lvbl91dWlkIjoiNjBiZWY0MjciLCJpZCI6MTI3ODIxNDksImVtYWlsIjoiaGFyZHdvcmtpbmdnZW5pdXNlc0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImhhcmR3b3JraW5nZ2VuaXVzZXMiLCJ1c2VyX3NsdWciOiJoYXJkd29ya2luZ2dlbml1c2VzIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2hhcmR3b3JraW5nZ2VuaXVzZXMvYXZhdGFyXzE3MTExNTIzNzEucG5nIiwicmVmcmVzaGVkX2F0IjoxNzUzMDQyODU1LCJpcCI6IjI2MDM6ODA4MDoxZDAwOjRiODE6OWM3Zjo1MzY1OmQ4Y2U6YjFmYSIsImlkZW50aXR5IjoiY2U2OWI4NTFjNGVkYzdlZWJmYjM5OThhYTk0YTcxNTciLCJkZXZpY2Vfd2l0aF9pcCI6WyJkYjZhYjE1MjZkMjA3NGJmZTVkZjQyNjU1OWQ1ZjMzOCIsIjI2MDM6ODA4MDoxZDAwOjRiODE6OWM3Zjo1MzY1OmQ4Y2U6YjFmYSJdfQ.CLtiWuIQzUWd28b8zJI-_WcalwQBCsht0tTnKlMPpX8; csrftoken=fsS1nKtxhptx2T1soDHVXcVu6rbwbEGpHq402UdkEVvyjDNhM5aKVLlKvceb588L"
    test_csrftoken = ""

    print(difficulty)
    print(topics)

    # Your logic to generate title, description from prompt
    # api_response = stream_format(prompt)
    # title = api_response['title']
    # description = api_response['description']
    title = "testing"
    description = "description"
    scheduled_time = datetime.datetime.fromisoformat(f"{date}T{time}")

    create_stream(title, description, scheduled_time, youtube)

    fetch_all_approved_unique_problem_names(hwg_cookies, test_csrftoken, output_path="approved_problems.txt")
    solved_problems = load_approved_problems("approved_problems.txt")
    problems = fetch_leetcode_questions(hwg_cookies, difficulty, topics, solved_problems=solved_problems)

    problems_payload = []

    for p in problems:
        problems_payload.append(f"{p['difficulty']} {p['title']} {p['acRate']}")

    return jsonify({'message': 'Stream scheduled!', 'problems_payload' : problems_payload}), 200

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.run(port=8080)
