# Web App related imports

from flask import Flask, send_from_directory, request
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


@app.route('/video', methods=['GET'])
def get_wdf_video():
    return send_from_directory(
        directory='./static/videos', path='Visualizer.mp4', mimetype='video/mp4', as_attachment=True)


@app.route('/simulation', methods=['POST'])
# TODO implement post request with all simulation parameters
def run_simulation():
    simulation_settings = request.json
    print('received from client: ', simulation_settings)
    scaled_parameters = Utils.parse_simulation_settings(simulation_settings)
    # simulator = Simulator(scaled_parameters)  # TODO: parse params from dictionary
    # visualizer = Visualizer()  # create Visualizer instance
    # result = simulator.run_simulation()
    # Settings.set_string(result[0])
    # Settings.set_hammer(result[1])
    # visualizer.render()


if __name__ == '__main__':
    app.run()
