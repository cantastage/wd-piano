# Web App related imports
from datetime import datetime

from flask import Flask, send_from_directory, request, make_response, jsonify, send_file
from flask_cors import CORS

from model.settings import Settings
from model.simulator import Simulator
from model.utils import Utils
from model.visualizer import Visualizer
from model.visualizer import set_visualizer_config
from model.data_service import DataService
import pandas as pd
import json
from matplotlib.figure import Figure
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/chart', methods=['GET'])
def get_daap_chart():
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # buf = BytesIO()
    path = os.path.join('media', 'images', 'chart')
    fig.savefig(os.path.join('media', 'images', 'chart.png'), format="png")
    return send_from_directory(directory='media/images', path='chart.png', mimetype="image/png", as_attachment=False)


@app.route('/strings', methods=['GET'])
def get_strings():
    df = pd.read_csv('./model/transpose.csv', encoding='utf-8')
    strings = df.to_json(orient='values')
    # json_strings = json.dumps(strings, indent=4)
    # strings = df.to_json(orient='columns')
    return make_response(strings, 200)


@app.route('/video/<filename>', methods=['GET'])
def get_wdf_video(filename):
    """
    Returns the video file to the client
    :param filename: the name of the video file
    :return:
    """
    return send_from_directory(
        directory='media/videos/1080p60', path=filename, mimetype='video/mp4', as_attachment=False)


@app.route('/simulation', methods=['POST'])
def run_simulation():
    """
    Requests the rendering of the wd-piano algorithm to the server
    """
    received_wd_parameters = request.json
    # print('received from client: ', received_wd_parameters)
    scaled = Utils.scale_wd_parameters(received_wd_parameters)
    Settings.set_wd_params(scaled['iterations'],
                           scaled['samplingFrequency'],
                           scaled['soundSpeed'],
                           scaled['stringFundamentalFrequency'],
                           scaled['stringTension'],
                           scaled['stringLength'],
                           scaled['stringDiameter'],
                           scaled['soundboardReflectionCoefficient'],
                           scaled['hammerMass'],
                           scaled['hammerRelativeStrikingPoint'],
                           scaled['hammerInitialVelocity'],
                           scaled['hammerStringDistance'],
                           scaled['linearFeltStiffness'])
    simulator = Simulator(scaled['iterations'],
                          scaled['samplingFrequency'],
                          scaled['soundSpeed'],
                          scaled['stringFundamentalFrequency'],
                          scaled['stringTension'],
                          scaled['stringLength'],
                          scaled['stringDiameter'],
                          scaled['soundboardReflectionCoefficient'],
                          scaled['hammerMass'],
                          scaled['hammerRelativeStrikingPoint'],
                          scaled['hammerInitialVelocity'],
                          scaled['hammerStringDistance'],
                          scaled['linearFeltStiffness'])
    result = simulator.run_simulation()
    Settings.set_string(result[0])
    Settings.set_hammer(result[1])
    video_filename = "WD-Piano-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".mp4"
    set_visualizer_config({"output_file": video_filename})
    visualizer = Visualizer()  # create Visualizer instance
    visualizer.render()
    return make_response(jsonify({'videoFilename': video_filename}), 200)


if __name__ == '__main__':
    app.run()
