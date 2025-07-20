from flask import Flask
from api.youtube import youtube_bp
# Other routes...

app = Flask(__name__)
app.register_blueprint(youtube_bp, url_prefix="/api/youtube")
