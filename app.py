# Web App related imports

from flask import Flask, send_from_directory, request, make_response, jsonify, url_for
from flask_cors import CORS

from model.simulator import Simulator
from model.settings import Settings
from model.utils import Utils
from model.visualizer import Visualizer

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/video/<filename>', methods=['GET'])
def get_wdf_video(filename):
    print('ENTRA QUI')
    return send_from_directory(
        directory='media', path=filename, mimetype='video/mp4', as_attachment=False)


# @app.route('/video', methods=['GET'])
# def get_wdf_video():
#     return send_from_directory(
#         directory='./static/videos', path='Visualizer.mp4', mimetype='video/mp4', as_attachment=True)


@app.route('/simulation', methods=['POST'])
# TODO implement post request with all simulation parameters
def run_simulation():
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
    visualizer = Visualizer()  # create Visualizer instance
    visualizer.render()
    # video_url = 'http://localhost:5000/media/videos/1080p60/Visualizer.mp4'
    video_filename = 'Visualizer.mp4'
    return make_response(jsonify({'videoFilename': video_filename}), 200)


if __name__ == '__main__':
    app.run()
