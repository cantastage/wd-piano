import numpy as np
import scipy.io as sio
import math


def dwg_shift(val, wg, n):
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

    :param val:
    :param k:
    :return:
    """
    if val < 0:
        out = -val
    else:
        out = (1 + 2 * k * val - math.sqrt(1 + 8 * k * val)) / (2 * k)
    return out


class Simulator:
    """
    Class modeling the piano hammer-string interaction
    """
    def __init__(self):
        self.iterations = np.uintc(88200)
        self.Fs = np.uintc(44100)
        self.Ts = np.double(1 / self.Fs)
        self.wg_length = np.uintc(168)
        self.wg_length_left = np.uintc(math.ceil(self.wg_length * 0.116))
        # print('wg_length_left: ', self.wg_length_left)
        self.wg_length_right = np.uintc(self.wg_length - self.wg_length_left)
        # print('wg_length_right: ', self.wg_length_right)
        self.K = np.double(0.98)  # soundboard reflection coefficient
        self.A = np.uintc(1000)  # linear felt stiffness TODO check if better int or float
        self.str_length = np.double(0.62)  # string length
        self.tension = np.double(670)
        self.hammer_initial_velocity = np.double(7)
        self.hs_distance = np.double(0.01)  # hammer-string distance
        self.Lh = np.double(3.93e-3)
        self.Z = np.double(10.28)  # characteristic impedance of the string

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
        self.wg_left = np.zeros(self.wg_length_left)
        # print('init wg_left shape is: ', self.wg_left.shape)
        # print(self.wg_left)
        self.wg_right = np.zeros(self.wg_length_right)
        # print('init wg_right_shape is: ', self.wg_right.shape)
        self.string = np.zeros(self.iterations)
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
        :return:

        """
        print('Starting WDF-Piano algorithm')
        print('Simulation will be run for: ', len(range(0, self.iterations)), ' steps')
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
        file_name = 'python_string_matrix.mat'
        print('Saving simulation output to: ', file_name)
        sio.savemat(file_name, {'python_string_matrix': self.string_matrix})
        return self.string_matrix, self.hammer

