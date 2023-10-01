# Standard library imports
import base64
from io import BytesIO

# Third party imports
from matplotlib.figure import Figure
import numpy as np


class StaticVisualizer:
    """
    Class that renders simulation data into a sequence of plots that can be visualized in the client
    """
    _piano_string_matrix: np.ndarray = None
    _hammer_positions: np.ndarray = None

    def __init__(self, string_data: np.ndarray, hammer_positions: np.ndarray):
        self._piano_string_matrix = string_data
        self._hammer_positions = hammer_positions

    def render_hs_plots(self) -> np.ndarray:
        """
        Renders the hammer-string interaction plots for slow-speed visualization
        :return hs_frames_b64: array containing base64 encoding of plots
        """
        hs_frames_b64 = np.empty(self._piano_string_matrix.shape[0])
        for i in range(0, self._piano_string_matrix.shape[0]):
            print('Starting rendering of hammer-string interaction')
            x = np.linspace(0, self._piano_string_matrix.shape[1], self._piano_string_matrix.shape[1])
            y = self._piano_string_matrix[i, :]
            fig = Figure()
            ax = fig.subplots()
            ax.plot(x, y)
            # TODO add axes and titles
            buf = BytesIO()
            fig.savefig(buf, format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            np.append(hs_frames_b64, data)  # Add new base64 image to array
        return hs_frames_b64
