# Web App related imports
from datetime import datetime

from flask import Flask, send_from_directory, request, make_response, jsonify
from flask_cors import CORS

from model.settings import Settings
from model.simulator import Simulator
from model.utils import Utils
from model.visualizer import Visualizer
from model.visualizer import set_visualizer_config

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


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
    # with tempconfig({"output_file": video_filename}):
    #     visualizer = Visualizer()  # create Visualizer instance
    #     visualizer.render()
    set_visualizer_config({"output_file": video_filename})
    visualizer = Visualizer()  # create Visualizer instance
    visualizer.render()
    # video_url = 'http://localhost:5000/media/videos/1080p60/Visualizer.mp4'
    return make_response(jsonify({'videoFilename': video_filename}), 200)


if __name__ == '__main__':
    app.run()
