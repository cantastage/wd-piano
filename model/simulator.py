import numpy as np
import scipy.io as sio
import math
import os
from datetime import datetime
from model.settings import Settings
import soundfile as sf


def dwg_shift(val: float, wg, n: int):
    """
    Updates the digital waveguide

    :param val: Incoming value
    :param wg: Waveguide to update
    :param n: index of the current step
    :return: last updated value of the waveguide
    """
    # m = np.remainder(n, wg.size)
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
        effective_wg_length = round(sampling_freq / (2*f0))  # it is the folded wg length
    else:
        # wg_length = L/X_s = L/(c/fs) = fs*L/c
        effective_wg_length = round((string_length / sound_speed) * sampling_freq)
    print('effective wg length (folded) is: ', effective_wg_length)
    effective_left_length = round(effective_wg_length * relative_hammer_position)
    effective_right_length = effective_wg_length - effective_left_length
    wg_left_length = effective_left_length * 2
    print('calculated left length: ', wg_left_length)
    wg_right_length = effective_right_length * 2
    print('calculated right length: ', wg_right_length)
    return wg_left_length, wg_right_length


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


class Simulator:
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
        wg_lengths = get_wg_lengths(wg_length_calc_mode,
                                    string_frequency,
                                    sampling_freq,
                                    hammer_relative_striking_point,
                                    string_length,
                                    sound_speed)
        self.wg_length_left = wg_lengths[0]
        print('wg_length_left: ', self.wg_length_left)
        self.wg_length_right = wg_lengths[1]
        print('wg_length_right: ', self.wg_length_right)
        self.wg_length = self.wg_length_left + self.wg_length_right  # NB: formula per wg_length: wg_length = Fs / f0
        print('Total waveguide length: ', self.wg_length)
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
        self.Knl = self.C * self.A  # TODO uncomment to return to previous condition
        # self.Knl = 1.347e9

        # Init waves
        self.wg_left = np.zeros(self.wg_length_left)
        # print('init wg_left shape is: ', self.wg_left.shape)
        self.wg_right = np.zeros(self.wg_length_right)
        # print('init wg_right_shape is: ', self.wg_right.shape)
        self.string = np.zeros(self.iterations)  # store values of string @ contact pt for audio file creation
        # print('init string shape is: ', self.string.shape)
        self.hammer = np.zeros(self.iterations)
        # print('init hammer shape is ', self.hammer.shape)

        # Init incident waves for strings
        self.a1 = 0
        self.a2 = 0
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
        # Settings.set_hammer_initial_position(self.hammer_initial_position)
        self.string_velocity = (self.a1 - self.b1) / self.Z1
        self.string_position = np.double(0)

        # init other values
        self.string_velocity_old = np.double(0)
        self.string_position_old = np.double(0)
        self.hammer_velocity_old = np.double(0)
        self.hammer_position_old = np.double(0)

        # matrix containing summed waveguide values at each iteration
        self.string_matrix = np.zeros((self.iterations, self.wg_length // 2))
        print('Initialized string matrix with shape: ', self.string_matrix.shape)
        print('total wgLength allocated length is: ', self.wg_length)
        print("Effective wgLength is: ", self.wg_length // 2)

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
            self.a1 = dwg_shift(-self.b1, self.wg_left, n)
            self.a2 = dwg_shift(self.K * self.b2, self.wg_right, n)

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

            # Fill string_matrix TODO verify array indexing is correct
            half_wg_left_length = self.wg_length_left // 2
            l1 = self.wg_left[0:half_wg_left_length]
            # print('self.wg_length_left // 2 is: ', self.wg_length_left // 2)
            # print('l1 size is: ', l1.size)
            l2 = self.wg_left[half_wg_left_length:self.wg_length_left]
            # print('l2 size is: ', l2.size)
            left = np.add(np.flip(l2), l1)
            # print('left size is: ', left.size)
            half_wg_right_length = self.wg_length_right // 2
            r1 = self.wg_right[0:half_wg_right_length]
            # print('r1 size is: ', r1.size)
            # print('self.wg_length_right // 2 is: ', self.wg_length_right // 2)
            r2 = self.wg_right[half_wg_right_length: self.wg_length_right]
            # print('r2 size is: ', r2.size)
            right = np.add(np.flip(r2), r1)
            # print('right size is: ', right.size)
            new_row = np.concatenate((left, right), axis=0)
            # self.string_matrix[n, :] = np.concatenate((left, right), axis=0)
            self.string_matrix[n, :] = new_row
            # print('new row @ step ', n, ' is: ', new_row)
            # print('string_matrix[', n, '] is: ', self.string_matrix[n, :])
            # self.string_matrix[n, 0:left.size] = left
            # self.string_matrix[n, left.size: self.string_matrix.shape[1]] = right
            # print('string_matrix[', n, '] size is: ', self.string_matrix[n].size)

        print('Ended WDF-Piano algorithm')
        # Creates a .mat file containing the string matrix
        # file_name = 'python_string_matrix.mat'
        # print('Saving simulation output to: ', file_name)
        # sio.savemat(file_name, {'python_string_matrix': self.string_matrix})

        # Create audio file with the string @ contact point
        print('Relative striking point:', Settings.get_hammer_relative_striking_point())
        print('string wg length is: ', self.wg_length)
        wg_striking_point = round((self.wg_length/2)*Settings.get_hammer_relative_striking_point())
        Settings.set_wg_striking_point(wg_striking_point)
        print('striking point in waveguide is ', wg_striking_point)

        base_filename = ("WD-Piano-" + datetime.now().strftime("%Y%m%d-%H%M%S.%f"))
        Settings.set_base_filename(base_filename)  # set base filename in settings
        audio_file_name = base_filename + '.wav'  # append .wav extension
        audiofile_save_path = os.path.join('media', 'audio', audio_file_name)
        # SAVE AUDIO FILE WITH SOUNDFILE
        # sf.write(audiofile_save_path, self.string, samplerate=44100, subtype='PCM_24')  # we use soundfile
        # scaled_string = np.int16(self.string / np.max(np.abs(self.string)) * 32767)
        scaled_string = self.string / np.max(np.abs(self.string))*32767
        sio.wavfile.write(audiofile_save_path, self.Fs, scaled_string.astype(np.int16))

        # sio.wavfile.write(audiofile_save_path, self.Fs, self.string)
        # print('Saved audio file to: ', audiofile_save_path)
        return self.string_matrix, self.hammer
