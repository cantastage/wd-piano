"""
Class containing all the settings for the simulation and other globals
NOTE: due to manim library limitations (cannot pass arguments to scene)
we need to store here all global variables
"""


class Settings(object):
    _instance = None  # singleton instance
    _string = None
    _hammer = None
    _sampling_freq = 44100

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    # Getters
    @classmethod
    def get_string(cls):
        return cls._string

    @classmethod
    def get_hammer(cls):
        return cls._hammer

    @classmethod
    def get_sampling_freq(cls):
        return cls._sampling_freq

    # Setters
    @classmethod
    def set_string(cls, string):
        cls._string = string

    @classmethod
    def set_hammer(cls, hammer):
        cls._hammer = hammer

    @classmethod
    def set_sampling_freq(cls, sampling_freq):
        cls._sampling_freq = sampling_freq

