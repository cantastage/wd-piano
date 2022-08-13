from flask import Flask, send_from_directory, Response, url_for, jsonify
from flask_cors import CORS
import math
import numpy as np
from manim import *


def shift_wg(val, vector, n, length):
    if n > length:
        m = n - np.floor(n/length)*length + 1
    else:
        m = n

    out = vector[m]
    vector[m] = val
    return out, vector


def nl_felt(val, k):
    return 1 + 2 * k * val - math.sqrt(1 + 8 * k * val) / (2 * k)


class Simulator:
    iterations = 88200
    Fs = 44100
    Ts = 1 / Fs
    wgLength = 168
    wgLengthLeft = math.ceil(wgLength * 0.116)
    wgLengthRight = wgLength - wgLengthLeft
    K = 0.98
    A = 1000
    str_length = 0.62
    tension = 670
    hammer_initial_velocity = 7
    hs_distance = 0.01
    Lh = 3.93e-3
    Z = 10.28

    # Adaptations conditions
    Z1 = Z
    Z2 = Z
    Z3 = Z1 + Z2
    gammaSer = Z1 / Z3
    Z4 = Z3
    Z5 = 2 * Lh / Ts
    Z6 = Z4 * Z5 / (Z4 + Z5)
    gammaPar = Z6 / Z4
    C = Ts / (2 * Z6)
    Z7 = Z6

    felt_slope = (A * C - 1) / (A * C + 1)
    Knl = C * A

    wgLeft = np.zeros(wgLengthLeft)
    wgRight = np.zeros(wgLengthRight)
    string = np.zeros(iterations)
    hammer = np.zeros(iterations)

    a1 = 0
    a2 = 0
    b3 = -a1 - a2
    a4 = b3
    a5 = Z5 * hammer_initial_velocity / 2
    b6 = a5 - gammaPar * (a5 - a4)
    a7 = b6
    b8 = - hs_distance / (2 * C)
    wave_integrator_delay_old = b8 - a7
    a8 = nl_felt(b8, felt_slope)
    wave_integrator_delay = a7 - a8
    b7 = a8 + wave_integrator_delay_old
    a6 = b7
    b5 = a6 - gammaPar * (a5 - a4)
    b4 = -a4 + a5 + b5
    a3 = b4
    b1 = a1 - gammaSer * (a1 + a2 + a3)
    b2 = -a3 - b1

    hammer_velocity = (a5 - b5) / Z5
    hammer_position = (b8 - a8) * C
    hammer_initial_position = hammer_position
    string_velocity = (a1 - b1) / Z1
    string_position = 0

    string_matrix = np.zeros((iterations, int(wgLength / 2)))
    # init other values
    string_velocity_old = 0
    hammer_velocity_old = 0
    hammer_position_old = 0
    string_position_old = 0

    def run_simulation(self):
        for n in range(1, self.iterations):
            wg_left_new_values = shift_wg(-self.b1, self.wgLeft, n, self.wgLengthLeft)
            self.a1 = wg_left_new_values[0]
            self.wgLeft = wg_left_new_values[1]
            wg_right_new_values = shift_wg(self.K * self.b2, self.wgRight, n, self.wgLengthRight)
            self.a2 = wg_right_new_values[0]
            self.wgRight = wg_right_new_values[1]

            self.wave_integrator_delay_old = self.wave_integrator_delay
            self.string_velocity_old = self.string_velocity
            self.string_position_old = self.string_position
            self.hammer_velocity_old = self.hammer_velocity
            self.hammer_position_old = self.hammer_position

            self.b3 = -self.a1 - self.a2
            self.a4 = self.b3
            self.a5 = -self.b5
            self.b6 = self.a5 - self.gammaPar*(self.a5 - self.a4)
            self.a7 = self.b6
            self.b8 = self.a7 + self.wave_integrator_delay_old
            self.a8 = nl_felt(self.b8, self.Knl)
            self.wave_integrator_delay = self.a7 - self.a8
            self.b7 = self.a8 + self.wave_integrator_delay_old
            self.a6 = self.b7
            self.b5 = self.a6 - self.gammaPar*(self.a5 - self.a4)
            self.b4 = -self.a4 + self.a5 + self.b5
            self.a3 = self.b4
            self.b1 = self.a1 - self.gammaSer*(self.a1 + self.a2 + self.a3)
            self.b2 = -self.a3 - self.b1

            self.string_velocity = (self.a1 - self.b1)/self.Z1
            self.string_position = self.string_position_old + (self.string_velocity + self.string_velocity_old)*self.Ts/2
            self.string[n] = self.string_position
            self.hammer_velocity = (self.a5 - self.b5)/self.Z5
            self.hammer_position = self.hammer_position_old + (self.hammer_velocity + self.hammer_velocity_old)* self.Ts / 2
            self.hammer[n] = self.hammer_position
            # fill string_matrix TODO verify array indexing is correct
            x = np.array(1, self.wgLength/2)
            l1 = self.wgLeft[0:self.wgLengthLeft/2 - 1]
            l2 = self.wgLeft[self.wgLengthLeft/2:self.wgLengthLeft - 1]
            left = np.flip(l2) + l1
            r1 = self.wgRight[1:self.wgLengthRight/2 - 1]
            r2 = self.wgRight[self.wgLengthRight/2: self.wgLengthRight-1]
            right = np.flip(r2) + r1
            self.string_matrix[n][:] = np.concatenate(left, right)
            return self.string_matrix


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
        directory='./static/videos', path='wdf-piano-example.mp4', mimetype='video/mp4', as_attachment=True)


if __name__ == '__main__':
    # simulator = Simulator()
    # matrix = simulator.run_simulation()
    # print('Obtained matrix from simulation is: ', matrix)
    app.run() #TODO uncomment to run web application
