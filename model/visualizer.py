import math
from typing import Dict
from manim import *
from model.settings import Settings

def set_visualizer_config(config_params: Dict):
    """
    Sets the manim config parameters for the visualizer

    :param config_params: the config parameters
    :return:
    """
    # Useful Config settings
    # config.custom_folders = True
    # config.media_dir = './static'
    config.renderer = 'opengl'
    config.write_to_movie = True
    config.flush_cache = True  # clear video cache
    config.disable_caching = True  # avoid using cached data
    # Unique for to set the config in manim config
    for k, v in config_params.items():
        config[k] = v


def plot_string_graph(string_matrix, axes, iteration_idx):
    """
    Plots the piano string graph

    :param string_matrix:
    :param axes:
    :param iteration_idx:
    :return:
    """
    repetition_counter = Settings.get_plot_repetition_counter()
    real_row_idx = Settings.get_real_row_idx()
    if iteration_idx % Settings.get_video_scaling_factor() < repetition_counter:
        Settings.set_plot_repetition_counter(repetition_counter + 1)
    else:
        Settings.set_plot_repetition_counter(0)
        Settings.set_real_row_idx(real_row_idx + 1)
    # NOTA: per le colonne si conta x - 1 poichè le coordinate dell'asse sono indicizzate a partire da 1
    return axes.plot(lambda x: string_matrix[Settings.get_real_row_idx()][int(x) - 1], color=RED)


def get_hammer(hammer_matrix, axes, iteration_idx):
    """
    Draws the piano hammer

    :param hammer_matrix: the array containing the hammer positions
    :param axes: the axes system where the hammer is plot
    :param iteration_idx: index of the hammer position array
    :return:
    """
    repetition_counter = Settings.get_plot_repetition_counter()
    real_position_idx = Settings.get_real_row_idx()
    if iteration_idx % Settings.get_video_scaling_factor() < repetition_counter:
        Settings.set_plot_repetition_counter(repetition_counter + 1)
    else:
        Settings.set_plot_repetition_counter(0)
        Settings.set_real_row_idx(real_position_idx + 1)
        
    center_y_coord = hammer_matrix[Settings.get_real_row_idx()] * 100
    center_x_coord = Settings.get_wg_striking_point()

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
        string_max_value = np.max(np.abs(string))  # add check on negative max value using abs
        hammer_max_value = np.max(hammer_positions)
        max_y_coord = math.ceil(max(string_max_value, hammer_max_value))
        axes = Axes(
            x_range=[0, string_shape[1], 1],
            y_range=[-max_y_coord, max_y_coord, 1],
            tips=False
        )
        # axes.add_coordinates()
        axes_labels = axes.get_axis_labels()
        idx_tracker = ValueTracker(-1)  # initialize value tracker TODO check correct start value
        string_graph = always_redraw(lambda: plot_string_graph(string, axes, idx_tracker.get_value()))

        # string_label = axes.get_graph_label(string_graph, label='PIANO STRING')
        # plot = VGroup(axes, string_graph)
        # plot = VGroup(string_graph, axes_labels)
        # labels = VGroup(axes_labels)
        print('hammer_positions[0]: ', hammer_positions[0])
        hammer = always_redraw(lambda: get_hammer(hammer_positions, axes, idx_tracker.get_value()))

        self.add(string_graph, hammer)

        scaling_factor = Settings.get_video_scaling_factor()
        shown_percentage = Settings.get_video_percentage()
        duration = (Settings.get_iterations() / Settings.get_sampling_freq() * scaling_factor) / 100 * shown_percentage
        value_tracker_iterations = (string_shape[0])/100*shown_percentage
        self.wait()
        # self.play(ApplyMethod(idx_tracker.increment_value, (string_shape[0])),
        #           run_time=period * (string_shape[0]))
        self.play(ApplyMethod(idx_tracker.increment_value, value_tracker_iterations), run_time=duration)
        self.wait()
        Settings.set_real_row_idx(0)
        Settings.set_plot_repetition_counter(0)

