class Settings(object):
    """
    This class contains some global variables needed by the application
    """
    _instance = None  # singleton instance
    _string = None
    _hammer = None
    _sampling_freq = 44100
    _hammer_initial_position: float = 0.0

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

    @classmethod
    def get_hammer_initial_position(cls):
        return cls._hammer_initial_position

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

    @classmethod
    def set_hammer_initial_position(cls, hammer_initial_position):
        cls._hammer_initial_position = hammer_initial_position
