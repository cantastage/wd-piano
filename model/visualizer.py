import math
from typing import Dict
import os

import manim
from manim import *
from model.settings import Settings


def set_visualizer_config(config_params: Dict):
    """
    Sets the manim config parameters for the visualizer

    :param config_params: the config parameters
    :return:
    """
    # Useful Config settings #TODO remove after finished
    # config.custom_folders = True
    # config.media_dir = './static'
    # config.output_file = 'prova-video.mp4'
    config.renderer = 'opengl'
    config.write_to_movie = True
    config.flush_cache = True  # TODO check if this is needed
    config.disable_caching = True  # TODO check if this is needed
    # TODO maybe add consistency checks or let the function accept only the required parameters
    # Unique for to set the config in manim config
    for k, v in config_params.items():
        config[k] = v


def plot_string_graph(string_matrix, axes, row_idx):
    """
    Plots the piano string graph

    :param string_matrix:
    :param axes:
    :param row_idx:
    :return:
    """

    # print("plotting row: ", int(row_idx))
    # NOTA: per le colonne si conta x - 1 poichè le coordinate dell'asse sono indicizzate a partire da 1
    # if (row_idx % 2 != 0) and (row_idx > 0):
    #     # since we doubled the length of animation it means we have real frames in even idxs while odd ones
    #     return axes.plot(lambda x: string_matrix[int(row_idx)][int(x) - 2], color=RED)
    # else:
    #     return axes.plot(lambda x: string_matrix[int(row_idx)][int(x) - 1], color=RED)
    return axes.plot(lambda x: string_matrix[int(row_idx)][int(x) - 1], color=RED)


def get_hammer(hammer_matrix, axes, position_idx):
    """
    Draws the piano hammer

    :param hammer_matrix: the array containing the hammer positions
    :param axes: the axes system where the hammer is plot
    :param position_idx: index of the hammer position array
    :return:
    """
    center_y_coord = hammer_matrix[int(position_idx) - 1]
    center_x_coord = Settings.get_wg_striking_point()
    # center_x_coord = 19
    center_point = Dot(axes.c2p(center_x_coord, center_y_coord, 0))
    circle = Circle(color=BLUE, fill_color=BLUE, fill_opacity=1.0).surround(center_point, buffer_factor=2.0)
    circle.move_to(circle.get_bottom())
    return circle


class Visualizer(Scene):
    """
    Class used to visualize Piano Hammer-String Interaction
    """

    #  TODO find if you can pass string-hammer matrices directly to Scene or you need to encapsulate it in superclass
    def construct(self):
        # -------------- PYTHON DATA --------------------------------------#
        period = 1 / Settings.get_sampling_freq()  # calculated from settings TODO check if needs to be given as param

        string = Settings.get_string()  # string matrix
        hammer_positions = Settings.get_hammer()  # hammer matrix

        string_shape = string.shape  # get string matrix shape to calculate max value
        print('string_shape = ', string_shape)
        string_max_value = np.max(string)  # add check on negative max value using abs
        print('string_max_value = ', string_max_value)
        hammer_max_value = np.max(hammer_positions)
        print('hammer_max_value = ', hammer_max_value)
        max_y_coord = math.ceil(max(string_max_value, hammer_max_value))
        print('max_y_coord = ', max_y_coord)
        # TODO check parameters of axes to get optimal view
        axes = Axes(
            x_range=[0, string_shape[1], 1],
            y_range=[-max_y_coord, max_y_coord, 1],
            tips=False
        )
        # axes.add_coordinates()
        axes_labels = axes.get_axis_labels()
        idx_tracker = ValueTracker(0)  # initialize value tracker
        string_graph = always_redraw(lambda: plot_string_graph(string, axes, idx_tracker.get_value()))

        # string_label = axes.get_graph_label(string_graph, label='PIANO STRING')
        # plot = VGroup(axes, string_graph)
        # plot = VGroup(string_graph, axes_labels)
        # labels = VGroup(axes_labels)
        print('hammer_positions[0]: ', hammer_positions[0])
        # hammer_center_point = Dot(point=axes.c2p(19, 0, 0), color=YELLOW)
        hammer = always_redraw(lambda: get_hammer(hammer_positions, axes, idx_tracker.get_value()))

        # self.add(string_graph, hammer, hammer_center_point)
        self.add(string_graph, hammer)
        print('Visualizer: string shape:', Settings.get_string().shape)
        print('Visualizer: hammer shape:', Settings.get_hammer().shape)
        # print('Visualizer: string sj:', np.max(Settings.get_string()))

        # add sound
        audio_file_path = os.path.join('media', 'audio', Settings.get_base_filename() + '.wav')
        self.add_sound(audio_file_path, time_offset=1, gain=1)  # TODO check time_offset to align sound to vid
        self.wait()
        # animation_run_time = 5  # TODO set to fs*duration
        # self.play(ApplyMethod(idx_tracker.increment_value, (string_shape[0] - 1)),
        #           run_time=period * (string_shape[0] - 1))
        scaling_factor = 160
        duration = (Settings.get_iterations() / Settings.get_sampling_freq() * scaling_factor)/100*4
        iterations_value_tracker = (string_shape[0])/100*25
        print('iterations value tracker:  ', iterations_value_tracker)
        self.play(ApplyMethod(idx_tracker.increment_value, iterations_value_tracker), run_time=duration)
        self.wait()
