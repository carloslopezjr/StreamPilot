from flask import session
from api.openai.openai_api import gen_desc
import os

def stream_format(prompt):
    api_response = gen_desc(prompt) # change prompt to what user wants

    title = api_response['title']
    description = api_response['description']

    return ({"title": title, "description" : description})

def create_stream(title, description, scheduled_time, youtube, thumbnail_path=None):

    # 1. Create broadcast
    broadcast = youtube.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "scheduledStartTime": scheduled_time.isoformat() + "Z"
            },
            "status": {
                "privacyStatus": "public"
            },
            "contentDetails": {
                "enableAutoStart": True,
                "enableAutoStop": True
            }
        }
    ).execute()

    # 2. Create stream
    stream = youtube.liveStreams().insert(
        part="snippet,cdn",
        body={
            "snippet": {
                "title": f"{title} Stream"
            },
            "cdn": {
                "frameRate": "30fps",
                "resolution": "720p",
                "ingestionType": "rtmp"
            }
        }
    ).execute()

    # 3. Bind
    youtube.liveBroadcasts().bind(
        part="id,contentDetails",
        id=broadcast["id"],
        streamId=stream["id"]
    ).execute()

    # 4. Upload thumbnail
    if thumbnail_path:
        youtube.thumbnails().set(
            videoId=broadcast["id"],
            media_body=thumbnail_path
        ).execute()

    return broadcast["id"], f"https://www.youtube.com/watch?v={broadcast['id']}"
