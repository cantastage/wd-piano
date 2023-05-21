from typing import Dict

import numpy as np
from numpy import uintc, float_

'''
    This file contains the parameters used for the simulation
'''
simulation_parameters: dict[str, uintc | float_] = {
    'iterations': np.uintc(88200),
    'Fs': np.uintc(44100),
    'stringFundamentalFreq': np.float_(262.22),
}

#  piano_strings: Dict[str, Dict[str, float_]] = {
