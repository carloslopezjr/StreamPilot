from flask import Blueprint, request, jsonify
from .stream import schedule_stream
import datetime

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    title = data['title']
    description = data['description']
    scheduled_time = datetime.datetime.fromisoformat(data['time'])
    thumbnail_path = data.get('thumbnailPath')

    stream_id, stream_url = schedule_stream(title, description, scheduled_time, thumbnail_path)
    return jsonify({"stream_id": stream_id, "url": stream_url})
