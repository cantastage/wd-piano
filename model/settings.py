class Settings(object):
    """
    This class contains some global variables needed by the application
    """
    _instance = None  # singleton instance
    _string = None  # string matrix containing data to be plotted
    _hammer = None  # hammer matrix containing data to be plotted
    _iterations = 88200
    _sampling_frequency = 44100  # Hz
    _sound_speed = 331  # m/s @ 0.0 degrees Celsius
    _string_fundamental_freq = 262.22  # Hz
    _string_tension = 670  # Newtons
    _string_length = 0.657  # meters
    _string_diameter = 1.064e-3  # meters
    _string_volumetric_density = 7850  # kg/m^3
    _soundboard_reflection_coefficient = 0.98
    _hammer_mass = 8.71e-3  # kilograms
    _hammer_relative_striking_point = 0.116  # relative to string length
    _hammer_initial_velocity = 7  # m/s
    _hammer_string_distance = 0.01  # meters
    _linear_felt_stiffness = 1000  # N/m

    def __new__(cls):
        """
        This method implements the singleton pattern
        """
        if not hasattr(cls, 'instance'):
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_string(cls):
        return cls._string

    # -------------- Getters -------------- #
    @classmethod
    def get_hammer(cls):
        return cls._hammer

    @classmethod
    def get_iterations(cls):
        return cls._iterations

    @classmethod
    def get_sampling_freq(cls):
        return cls._sampling_frequency

    @classmethod
    def set_simulation_settings(cls, iterations,
                                sampling_frequency,
                                sound_speed,
                                string_fundamental_freq,
                                string_tension,
                                string_length,
                                string_diameter,
                                string_volumetric_density,
                                soundboard_reflection_coefficient,
                                hammer_mass,
                                linear_felt_stiffness,
                                hammer_relative_striking_point,
                                hammer_initial_velocity,
                                hammer_string_distance):
        """
        This method sets all the simulation parameters in one call
        """
        cls._iterations = iterations
        cls._sampling_frequency = sampling_frequency
        cls._sound_speed = sound_speed
        cls._string_fundamental_freq = string_fundamental_freq
        cls._string_tension = string_tension
        cls._string_length = string_length
        cls._string_diameter = string_diameter
        cls._string_volumetric_density = string_volumetric_density
        cls._soundboard_reflection_coefficient = soundboard_reflection_coefficient
        cls._hammer_mass = hammer_mass
        cls._hammer_relative_striking_point = hammer_relative_striking_point
        cls._hammer_initial_velocity = hammer_initial_velocity
        cls._hammer_string_distance = hammer_string_distance
        cls._linear_felt_stiffness = linear_felt_stiffness

    @classmethod
    def get_string_fundamental_freq(cls):
        return cls._string_fundamental_freq

    @classmethod
    def get_string_tension(cls):
        return cls._string_tension

    @classmethod
    def get_string_length(cls):
        return cls._string_length

    @classmethod
    def get_string_diameter(cls):
        return cls._string_diameter

    @classmethod
    def get_soundboard_reflection_coefficient(cls):
        return cls._soundboard_reflection_coefficient

    @classmethod
    def get_hammer_mass(cls):
        return cls._hammer_mass

    @classmethod
    def get_linear_felt_stiffness(cls):
        return cls._linear_felt_stiffness

    @classmethod
    def get_hammer_relative_striking_point(cls):
        return cls._hammer_relative_striking_point

    @classmethod
    def get_hammer_string_distance(cls):
        return cls._hammer_string_distance

    @classmethod
    def get_hammer_initial_velocity(cls):
        return cls._hammer_initial_velocity

    @classmethod
    def get_string_volumetric_density(cls):
        return cls._string_volumetric_density

    @classmethod
    def get_sound_speed_in_air(cls):
        return cls._sound_speed

    @classmethod
    def get_spatial_sampling_step(cls):
        return cls.get_sound_speed_in_air() / cls.get_sampling_freq()

    # -------------- Setters -------------- #
    @classmethod
    def set_string(cls, string):
        cls._string = string

    @classmethod
    def set_hammer(cls, hammer):
        cls._hammer = hammer

    # @classmethod
    # def set_sampling_freq(cls, sampling_freq):
    #     cls._sampling_freq = sampling_freq
    #
    # @classmethod
    # def set_hammer_initial_position(cls, hammer_initial_position):
    #     cls._hammer_initial_position = hammer_initial_position
