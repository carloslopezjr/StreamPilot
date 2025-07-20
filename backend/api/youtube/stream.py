# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from flask import session
# import datetime

# def get_authenticated_service(token):
#     creds = token  # Load from session or DB
#     return build("youtube", "v3", credentials=creds)

# def schedule_stream(title, description, scheduled_time, thumbnail_path=None):
#     youtube = get_authenticated_service(session['token'])

#     # 1. Create broadcast
#     broadcast = youtube.liveBroadcasts().insert(
#         part="snippet,status,contentDetails",
#         body={
#             "snippet": {
#                 "title": title,
#                 "description": description,
#                 "scheduledStartTime": scheduled_time.isoformat() + "Z"
#             },
#             "status": {
#                 "privacyStatus": "public"
#             },
#             "contentDetails": {
#                 "enableAutoStart": True,
#                 "enableAutoStop": True
#             }
#         }
#     ).execute()

#     # 2. Create stream
#     stream = youtube.liveStreams().insert(
#         part="snippet,cdn",
#         body={
#             "snippet": {
#                 "title": f"{title} Stream"
#             },
#             "cdn": {
#                 "frameRate": "30fps",
#                 "resolution": "720p",
#                 "ingestionType": "rtmp"
#             }
#         }
#     ).execute()

#     # 3. Bind
#     youtube.liveBroadcasts().bind(
#         part="id,contentDetails",
#         id=broadcast["id"],
#         streamId=stream["id"]
#     ).execute()

#     # 4. Upload thumbnail
#     if thumbnail_path:
#         youtube.thumbnails().set(
#             videoId=broadcast["id"],
#             media_body=thumbnail_path
#         ).execute()

#     return broadcast["id"], f"https://www.youtube.com/watch?v={broadcast['id']}"
