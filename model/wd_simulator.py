import numpy as np
import scipy.io as sio
import math
import os
from datetime import datetime
from model.settings import Settings


def dwg_shift(val: float, wg, n: int):
    """
    Updates the digital waveguide

    :param val: Incoming value
    :param wg: Waveguide to update
    :param n: index of the current step
    :return: last updated value of the waveguide
    """
    m = n % wg.size
    out = wg[m]
    wg[m] = val
    return out


def nl_felt(val, k):
    """
    Models the response of a nonlinear piano hammer felt

    :param val: incoming waveguide value
    :param k: Felt's nonlinear elasticity coefficient
    :return: felt's response value
    """
    if val < 0:
        out = -val
    else:
        out = (1 + 2 * k * val - math.sqrt(1 + 8 * k * val)) / (2 * k)
    return out


def get_wg_lengths(length_calc_mode: int,
                   f0: float,
                   sampling_freq: int,
                   relative_hammer_position: float,
                   string_length: float,
                   sound_speed: float) -> (int, int):
    """
    Calculates the length of the left and right part of the waveguide given:

    :param length_calc_mode: wg_length calculation mode
    :param f0: fundamental frequency of the string
    :param sampling_freq: sampling frequency
    :param relative_hammer_position: relative position of the hammer on the string
    :param string_length: length of the string
    :param sound_speed: speed of sound in the medium
    :return: length of the left and right part of the waveguide
    """
    if length_calc_mode == 0:
        total_wg_length = sampling_freq / (2 * f0)  # it is the folded wg length
    else:
        # wg_length = L/X_s = L/(c/fs) = fs*L/c
        total_wg_length = ((string_length / sound_speed) * sampling_freq)
    print('total wg length (unfolded) is = ', total_wg_length, ' samples')
    folded_wg_length = int(round(total_wg_length / 2))
    print('folded wg length is = ', folded_wg_length, ' samples')
    left_length = int(round(folded_wg_length * relative_hammer_position))
    if left_length == 0:
        left_length = 1
    right_length = folded_wg_length - left_length
    print('left length is = ', left_length, ' samples')
    print('right length is = ', right_length, ' samples')
    return left_length, right_length


def get_string_impedance(string_tension: float, string_diameter: float, string_volumetric_density: float) -> float:
    """
    Calculates the characteristic impedance of the string

    :param string_tension: the tension of the string in N
    :param string_diameter: the diameter of the string in m
    :param string_volumetric_density: the linear mass density of the string in kg/m
    :return: the characteristic impedance of the string in Ns/m
    """
    string_section = math.pi * (string_diameter / 2) ** 2
    string_linear_density = string_volumetric_density * string_section
    string_characteristic_impedance = math.sqrt(string_tension * string_linear_density)
    return string_characteristic_impedance


class WDSimulator:
    """
    Class modeling the piano hammer-string interaction
    """

    def __init__(self, iterations: int,
                 sampling_freq: int,
                 sound_speed: float,
                 string_frequency: float,
                 string_tension: float,
                 string_length: float,
                 string_diameter: float,
                 soundboard_reflection_coefficient: float,
                 hammer_mass: float,
                 hammer_relative_striking_point: float,
                 hammer_initial_velocity: float,
                 hammer_string_distance: float,
                 linear_felt_stiffness: float,
                 wg_length_calc_mode: int):
        self.iterations = iterations  # set number of iterations
        self.Fs = sampling_freq  # set sampling frequency
        self.Ts = np.double(1 / self.Fs)  # sampling period calculated from sampling frequency

        # # Calculate waveguide lengths TODO half the length to get right frequency
        # self.wg_length = 84  # TODO parametrize after debug
        # self.left_length = 16  # TODO parametrize after debug
        # self.right_length = 68  # TODO parametrize after debug
        # # upper rail and lower rail have the same length
        self.left_length, self.right_length = get_wg_lengths(wg_length_calc_mode,
                                                             string_frequency,
                                                             sampling_freq,
                                                             hammer_relative_striking_point,
                                                             string_length,
                                                             sound_speed)
        self.wg_length = self.left_length + self.right_length
        self.upper_rail = np.zeros(self.wg_length)
        self.lower_rail = np.zeros(self.wg_length)
        self.K = soundboard_reflection_coefficient  # set soundboard reflection coefficient
        self.A = linear_felt_stiffness  # set linear felt stiffness
        self.str_length = string_length  # string length in m
        self.tension = string_tension
        self.hammer_initial_velocity = hammer_initial_velocity
        self.hs_distance = hammer_string_distance  # hammer-string distance
        self.Lh = hammer_mass  # hammer mass inductance in kg
        self.Z = get_string_impedance(string_tension, string_diameter, Settings.get_string_volumetric_density())

        # Adaptations conditions (connection of WDF blocks)
        self.Z1 = self.Z
        self.Z2 = self.Z
        self.Z3 = self.Z1 + self.Z2
        self.gamma_ser = self.Z1 / self.Z3
        self.Z4 = self.Z3
        self.Z5 = 2 * self.Lh / self.Ts
        self.Z6 = self.Z4 * self.Z5 / (self.Z4 + self.Z5)
        self.gamma_par = self.Z6 / self.Z4
        self.C = self.Ts / (2 * self.Z6)  # Ref. capacitance of the mutator for the NL spring
        self.Z7 = self.Z6

        self.felt_slope = (self.A * self.C - 1) / (self.A * self.C + 1)
        self.Knl = self.C * self.A

        # Init waves
        self.string = np.zeros(self.iterations)  # store values of string @ contact pt for audio file creation
        self.hammer = np.zeros(self.iterations)  # store values of hammer positions for visualization

        # Init incident waves for strings
        self.a1 = 0  # value entering series junction from left
        self.a2 = 0  # value entering series junction from right
        self.b3 = -self.a1 - self.a2
        self.a4 = self.b3
        self.a5 = self.Z5 * self.hammer_initial_velocity / 2
        self.b6 = self.a5 - self.gamma_par * (self.a5 - self.a4)
        self.a7 = self.b6
        self.b8 = -self.hs_distance / (2 * self.C)
        self.wave_integrator_delay_old = self.b8 - self.a7
        self.a8 = nl_felt(self.b8, self.felt_slope)
        self.wave_integrator_delay = self.a7 - self.a8
        self.b7 = self.a8 + self.wave_integrator_delay_old
        self.a6 = self.b7
        self.b5 = self.a6 - self.gamma_par * (self.a5 - self.a4)
        self.b4 = -self.a4 + self.a5 + self.b5
        self.a3 = self.b4
        self.b1 = self.a1 - self.gamma_ser * (self.a1 + self.a2 + self.a3)
        self.b2 = -self.a3 - self.b1

        self.hammer_velocity = (self.a5 - self.b5) / self.Z5
        self.hammer_position = (self.b8 - self.a8) * self.C
        self.hammer_initial_position = self.hammer_position
        self.string_velocity = (self.a1 - self.b1) / self.Z1
        self.string_position = np.double(0)

        # init other values
        self.string_velocity_old = np.double(0)
        self.string_position_old = np.double(0)
        self.hammer_velocity_old = np.double(0)
        self.hammer_position_old = np.double(0)

        # matrix containing summed waveguide values at each iteration
        self.string_matrix = np.zeros((self.iterations, self.wg_length))
        print('Initialized string matrix with shape: ', self.string_matrix.shape)

    def run_simulation(self):
        """
        Runs the simulation

        :return: string matrix containing summed waveguide values at each iteration for plotting
        :return: hammer matrix containing matrix positions at each iteration for plotting
        """
        print('Starting WDF-Piano algorithm')
        print('Algorithm will be run for: ', len(range(0, self.iterations)), ' steps')
        #  runs the simulation for specified number of iterations
        for n in range(0, self.iterations):
            #  Shifts the two waveguides
            # Manage left part of the waveguide
            self.a1 = self.upper_rail[self.left_length - 1]  # value enters from wg to junction
            self.upper_rail[1:self.left_length] = self.upper_rail[0:self.left_length - 1]  # shift values right
            self.upper_rail[0] = -self.lower_rail[0]  # lower rail value passes to upper rail
            self.lower_rail[0:self.left_length - 1] = self.lower_rail[1:self.left_length]  # shift values left
            self.lower_rail[self.left_length - 1] = self.b1  # value exits from wg to junction
            # Manage right part of the waveguide
            self.a2 = self.lower_rail[self.left_length + 1]  # value enters from wg to junction
            self.lower_rail[self.left_length + 1:self.wg_length - 1] = self.lower_rail[
                                                                       self.left_length + 2:self.wg_length]  # shift values left
            self.lower_rail[self.wg_length - 1] = self.K * self.upper_rail[
                self.wg_length - 1]  # value passes from upper rail to lower rail
            self.upper_rail[self.left_length + 2:self.wg_length] = self.upper_rail[
                                                                   self.left_length + 1:self.wg_length - 1]  # shift values right
            self.upper_rail[self.left_length + 1] = self.b2  # value exits from wg to junction
            # Previous values
            self.wave_integrator_delay_old = self.wave_integrator_delay
            self.string_velocity_old = self.string_velocity
            self.string_position_old = self.string_position
            self.hammer_velocity_old = self.hammer_velocity
            self.hammer_position_old = self.hammer_position

            self.b3 = -self.a1 - self.a2
            self.a4 = self.b3
            self.a5 = -self.b5
            self.b6 = self.a5 - self.gamma_par * (self.a5 - self.a4)
            self.a7 = self.b6
            self.b8 = self.a7 + self.wave_integrator_delay_old
            self.a8 = nl_felt(self.b8, self.Knl)
            self.wave_integrator_delay = self.a7 - self.a8
            self.b7 = self.a8 + self.wave_integrator_delay_old
            self.a6 = self.b7
            self.b5 = self.a6 - self.gamma_par * (self.a5 - self.a4)
            self.b4 = -self.a4 + self.a5 + self.b5
            self.a3 = self.b4
            self.b1 = self.a1 - self.gamma_ser * (self.a1 + self.a2 + self.a3)
            self.b2 = -self.a3 - self.b1

            self.string_velocity = (self.a1 - self.b1) / self.Z1
            self.string_position = self.string_position_old + (
                    self.string_velocity + self.string_velocity_old) * self.Ts / 2
            self.string[n] = self.string_position
            self.hammer_velocity = (self.a5 - self.b5) / self.Z5
            self.hammer_position = self.hammer_position_old + (
                    self.hammer_velocity + self.hammer_velocity_old) * self.Ts / 2
            self.hammer[n] = self.hammer_position  # Store hammer position at current iteration

            # Store summed waveguide values at current iteration
            new_row = np.add(self.upper_rail.copy(), self.lower_rail.copy())
            self.string_matrix[n, :] = new_row

        print('Ended WDF-Piano algorithm')

        # Create audio file with the string @ contact point
        # wg_striking_point = round((self.wg_length / 2) * Settings.get_hammer_relative_striking_point())
        wg_striking_point = self.left_length + 1
        Settings.set_wg_striking_point(wg_striking_point)
        base_filename = ("WD-Piano-" + datetime.now().strftime("%Y%m%d-%H%M%S.%f"))
        Settings.set_base_filename(base_filename)  # set base filename in settings
        audio_file_name = base_filename + '.wav'  # append .wav extension
        audiofile_save_path = os.path.join('media', 'audio', audio_file_name)

        scaled_string = self.string / np.max(np.abs(self.string)) * 32767
        sio.wavfile.write(audiofile_save_path, self.Fs, scaled_string.astype(np.int16))

        # Scale string and hammer data for low-speed visualization
        visualization_scaling_factor = Settings.get_video_scaling_factor()
        visualization_string = np.repeat(self.string_matrix, repeats=visualization_scaling_factor, axis=0)
        visualization_hammer = np.repeat(self.hammer, repeats=visualization_scaling_factor, axis=0)
        visualization_string = np.roll(visualization_string, shift=-1, axis=1) # shift string matrix to the left for visualization purposes
        visualization_hammer = np.roll(visualization_hammer, shift=-1, axis=0)
        return visualization_string, visualization_hammer
