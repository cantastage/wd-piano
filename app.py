from flask import Flask, send_from_directory, request, make_response, jsonify
from flask_cors import CORS
import pandas as pd

from model.daap import AudioFeatureExtractor
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


@app.route('/plot/<filename>', methods=['GET'])
def get_feature_plot(filename):
    return send_from_directory(directory='media/images', path=filename, mimetype="image/png", as_attachment=False)


@app.route('/strings', methods=['GET'])
def get_strings():
    df = pd.read_csv('./model/transpose.csv', encoding='utf-8')
    strings = df.to_json(orient='values')
    return make_response(strings, 200)


@app.route('/plots', methods=['POST'])
def update_plots():
    """
    Updates spectral feature plots
    :return: updated spectral feature plot urls
    """
    base_filename = request.json['baseFilename']
    spectral_params = request.json['spectralParams']
    plot_version_index = request.json['plotVersionIndex']
    spectral_features = AudioFeatureExtractor.extract_features(base_filename, spectral_params, plot_version_index)
    return make_response(jsonify({'daapFeatures': spectral_features}), 200)


@app.route('/compare-plots', methods=['POST'])
def update_compare_plots():
    base_filename = request.json['baseFilename']
    filenames = request.json['filenames']
    spectral_params = request.json['spectralParams']
    plot_version_index = request.json['plotVersionIndex']
    extracted_features = AudioFeatureExtractor.batch_extract_features(base_filename,
                                                                      filenames,
                                                                      spectral_params,
                                                                      plot_version_index)
    return make_response(jsonify({'daapFeatures': extracted_features}), 200)


@app.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """
    Returns the audio file to the client
    :param filename: the name of the audio file
    :return:
    """
    return send_from_directory(
        directory='media/audio', path=filename, mimetype='audio/wav', as_attachment=False)


@app.route('/simulation', methods=['POST'])
def run_simulation():
    """
    Requests the rendering of the wd-piano algorithm to the server
    """
    received_wd_parameters = request.json['wdParameters']
    received_spectral_parameters = request.json['spectralParameters']
    received_create_video = request.json['createVideo']
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
                          scaled['linearFeltStiffness'],
                          scaled['wgLengthMode'])
    result = simulator.run_simulation()  # Run simulation
    Settings.set_string(result[0])  # get string matrix
    Settings.set_hammer(result[1])  # get hammer positions vector
    #  first time plot version index is 0
    extracted_features = AudioFeatureExtractor.extract_features(Settings.get_base_filename(),
                                                                received_spectral_parameters,
                                                                0)
    video_filename = Settings.get_base_filename() + ".mp4"
    set_visualizer_config({"output_file": video_filename})
    if received_create_video:
        visualizer = Visualizer()  # create Visualizer instance
        visualizer.render()  # render visualizer scene
    return make_response(jsonify({
        'baseFilename': Settings.get_base_filename(),
        'videoFilename': video_filename,
        'paramSummary': [],
        'daapFeatures': extracted_features,
        'plotVersionIndex': 0,
        'showVideo': received_create_video
    }), 200)


if __name__ == '__main__':
    # app.run(host='172:20:10:3', port=5000, debug=True)
    app.run()
