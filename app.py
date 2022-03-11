import os.path

from flask import Flask, send_from_directory, Response, url_for, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/video', methods=['GET'])
def get_wdf_video():
    return send_from_directory(
        directory='./static/videos', path='wdf-piano-example.mp4', mimetype='video/mp4', as_attachment=True)


if __name__ == '__main__':
    app.run()
