from flask import Blueprint, request, jsonify
from api.openai.openai_api import gen_desc
# from .stream import schedule_stream

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/schedule', methods=['POST', 'GET'])
def schedule():
    # data = request.json
    # title = data['title']
    # description = data['description']
    # scheduled_time = datetime.datetime.fromisoformat(data['time'])
    # thumbnail_path = data.get('thumbnailPath')

    # stream_id, stream_url = schedule_stream(title, description, scheduled_time, thumbnail_path)
    # return jsonify({"stream_id": stream_id, "url": stream_url})
    print(gen_desc("I want to do a live stream that covers binary search"))
    return jsonify({"test":"hello world!"})
