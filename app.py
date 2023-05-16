# Web App related imports

from flask import Flask, send_from_directory, Response, url_for, jsonify
from flask_cors import CORS

# Visualizer related imports
from manim import *
from model.simulator import Simulator
from model.settings import Settings

# GLOBAL VARS
#  TODO redefine NOT as global variables
PERIOD = 1 / 44100
# global MATRIX
# global HAMMER

# ----- VISUALIZER PART ---------------


def plot_string_graph(string_matrix, axes, row_idx):
    """
    Plots the piano string graph

    :param string_matrix:
    :param axes:
    :param row_idx:
    :return:
    """

    print("plotting row: ", int(row_idx))
    # NOTA: per le colonne si conta x - 1 poichè le coordinate dell'asse sono indicizzate a partire da 1
    return axes.plot(lambda x: string_matrix[int(row_idx)][int(x) - 1], color=RED)


def get_hammer(hammer_matrix, axes, position_idx):
    """
    Draws the piano hammer

    :param hammer_matrix:
    :param axes:
    :param position_idx:
    :return:
    """
    # center_y_coord = hammer_matrix[0][int(position_idx) - 1]
    center_y_coord = hammer_matrix[int(position_idx) - 1]  # TODO comment when hammer is 2D matrix
    center_point = Dot(axes.c2p(19, center_y_coord, 0))
    circle = Circle(color=BLUE, fill_color=BLUE, fill_opacity=1.0).surround(center_point, buffer_factor=2.0)
    circle.move_to(circle.get_bottom())
    return circle


class Visualizer(Scene):
    """
    Class used to visualize Piano Hammer-String Interaction
    """
    #  TODO find if you can pass string-hammer matrices directly to Scene or you need to encapsulate it in superclass
    def construct(self):
        # Config settings
        # config.custom_folders = True
        # config.media_dir = './assets/esticazzi'
        # config.output_file = 'prova-video.mp4'
        # config.renderer = "opengl"
        # config.write_to_movie = True
        config.flush_cache = True
        config.disable_caching = True

        # -------------- PYTHON DATA --------------------------------------#
        # string = MATRIX  # string obtained from current simulation
        # hammer_positions = HAMMER  # PYTHON hammer
        string = Settings.get_string()
        hammer_positions = Settings.get_hammer()

        string_shape = string.shape
        string_max_value = np.max(string)
        # print('string max: ', string_max_value)
        # define axes NB y range needs to be specified in that way
        axes = Axes(
            x_range=[0, string_shape[1], 1],
            y_range=[-int(string_max_value), int(string_max_value), 1],
            # y_range=[-5, 5, 0.5],
            x_length=10,
            y_length=10,
            tips=False
        )
        # axes.add_coordinates()
        axes_labels = axes.get_axis_labels()
        idx_tracker = ValueTracker(0)
        string_graph = always_redraw(lambda: plot_string_graph(string, axes, idx_tracker.get_value()))

        # string_label = axes.get_graph_label(string_graph, label='PIANO STRING')
        # plot = VGroup(axes, string_graph)
        # plot = VGroup(string_graph, axes_labels)
        # labels = VGroup(axes_labels)
        hammer_center_point = Dot(point=axes.c2p(19, 0, 0), color=YELLOW)
        hammer = always_redraw(lambda: get_hammer(hammer_positions, axes, idx_tracker.get_value()))

        self.add(string_graph, hammer)

        # add sound
        # self.add_sound("string.wav", time_offset=1, gain=1)  # regolare time_offset in base al numero di wait effettuate prima che parta il video
        self.add_sound("python_audio_string.wav", time_offset=1, gain=1) # with python created audio
        self.wait()
        # TODO check se la duration dell'animazione deve essere di string_shape[0] o string_shape[0] - 1
        self.play(ApplyMethod(idx_tracker.increment_value, (string_shape[0] - 1)), run_time=PERIOD * (string_shape[0] - 1))
        self.wait()


# --- WEB APP PART ---


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    # simulator = Simulator()
    # matrix = simulator.run_simulation()
    # console.log('Obtained matrix from simulation is: ', matrix)
    return 'Hello World!'


@app.route('/video', methods=['GET'])
def get_wdf_video():
    return send_from_directory(
        directory='./static/videos', path='Visualizer.mp4', mimetype='video/mp4', as_attachment=True)


@app.route('/simulation', methods=['GET'])
def get_simulation_result():
    # global MATRIX  # to reference global variable
    # global HAMMER  # to reference global variable

    simulator = Simulator()  # create Simulator instance
    visualizer = Visualizer()  # create Visualizer instance
    result = simulator.run_simulation()
    # MATRIX = result[0]
    # HAMMER = result[1]
    Settings.set_string(result[0])
    Settings.set_hammer(result[1])
    visualizer.render()


if __name__ == '__main__':
    # simulator = Simulator()  # create Simulator instance
    # visualizer = Visualizer()  # create Visualizer instance
    # result = simulator.run_simulation()  # run simulation
    # MATRIX = result[0]
    # HAMMER = result[1]
    # visualizer.render()
    app.run()
