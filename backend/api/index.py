from flask import Flask
from api.youtube import youtube_bp
from api.leetcode.routes import leetcode_bp
# Other routes...

app = Flask(__name__)
app.register_blueprint(youtube_bp, url_prefix="/api/youtube")
app.register_blueprint(leetcode_bp, url_prefix="/api/leetcode")

# filepath: c:\stream-setup-automation\stream-setup-automation\backend\api\index.py
if __name__ == "__main__":
    app.run(debug=True)