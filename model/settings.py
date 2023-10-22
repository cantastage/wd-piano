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
    _base_filename = None  # filename of the simulation data, for video and audio file saving

    _effective_wg_length: int = None
    _wg_striking_point: int = None

    _video_scaling_factor = 160
    _video_percentage = 100

    _real_row_idx = 0
    _plot_repetition_counter = 0

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
    def get_real_row_idx(cls):
        return cls._real_row_idx

    @classmethod
    def get_plot_repetition_counter(cls):
        return cls._plot_repetition_counter

    @classmethod
    def set_wd_params(cls, iterations,
                      sampling_frequency,
                      sound_speed,
                      string_fundamental_frequency,
                      string_tension,
                      string_length,
                      string_diameter,
                      soundboard_reflection_coefficient,
                      hammer_mass,
                      hammer_relative_striking_point,
                      hammer_initial_velocity,
                      hammer_string_distance,
                      linear_felt_stiffness):
        """
        This method sets all the simulation parameters in one call
        """
        cls._iterations = iterations
        cls._sampling_frequency = sampling_frequency
        cls._sound_speed = sound_speed
        cls._string_fundamental_freq = string_fundamental_frequency
        cls._string_tension = string_tension
        cls._string_length = string_length
        cls._string_diameter = string_diameter
        # cls._string_volumetric_density = string_volumetric_density
        cls._soundboard_reflection_coefficient = soundboard_reflection_coefficient
        cls._hammer_mass = hammer_mass
        cls._hammer_relative_striking_point = hammer_relative_striking_point
        cls._hammer_initial_velocity = hammer_initial_velocity
        cls._hammer_string_distance = hammer_string_distance
        cls._linear_felt_stiffness = linear_felt_stiffness

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

    @classmethod
    def get_base_filename(cls):
        return cls._base_filename

    @classmethod
    def get_effective_wg_length(cls):
        return cls._effective_wg_length

    @classmethod
    def get_wg_striking_point(cls):
        return cls._wg_striking_point

    @classmethod
    def get_video_scaling_factor(cls):
        return cls._video_scaling_factor

    @classmethod
    def get_video_percentage(cls):
        return cls._video_percentage

    # -------------- Setters -------------- #

    @classmethod
    def set_string(cls, string):
        cls._string = string

    @classmethod
    def set_hammer(cls, hammer):
        cls._hammer = hammer

    @classmethod
    def set_base_filename(cls, filename):
        cls._base_filename = filename

    @classmethod
    def set_effective_wg_length(cls, effective_wg_length):
        cls._effective_wg_length = effective_wg_length

    @classmethod
    def set_wg_striking_point(cls, wg_striking_point):
        cls._wg_striking_point = wg_striking_point

    @classmethod
    def set_video_scaling_factor(cls, video_scaling_factor):
        cls._video_scaling_factor = video_scaling_factor

    @classmethod
    def set_video_percentage(cls, video_percentage):
        cls._video_percentage = video_percentage

    @classmethod
    def set_real_row_idx(cls, real_row_idx):
        cls._real_row_idx = real_row_idx

    @classmethod
    def set_plot_repetition_counter(cls, plot_repetition_counter):
        cls._plot_repetition_counter = plot_repetition_counter


    # @classmethod
    # def set_sampling_freq(cls, sampling_freq):
    #     cls._sampling_freq = sampling_freq
    #
    # @classmethod
    # def set_hammer_initial_position(cls, hammer_initial_position):
    #     cls._hammer_initial_position = hammer_initial_position
