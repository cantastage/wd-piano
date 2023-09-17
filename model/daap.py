#  Feature richieste: MFCCs, spectral centroid, spectral roll-off, spectral bandwidth, tonnetz, etc.
import os
import glob
import numpy as np
import librosa
from matplotlib.figure import Figure

from model.settings import Settings


class AudioFeatureExtractor(object):
    _instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._instance = super(AudioFeatureExtractor, cls).__new__(cls)
        return cls._instance

    @classmethod
    def extract_features(cls, base_filename: str, spectral_parameters: dict, plot_version_index) -> dict:
        """
        Extracts spectral features from the audio file
        :param base_filename: base filename to retrieve audio data and plots data
        :param spectral_parameters: the parameters for the extraction of the spectral features
        :param plot_version_index: progressive index of plot versions
        :return: the extracted features
        """
        bg_color = '#f2f2f2'
        # print('Arrived spectral parameters: ', spectral_parameters)
        if plot_version_index > 0:
            cls.clear_old_plots(base_filename)  # clear old plot files
        sr = Settings.get_sampling_freq()
        audio_filename = base_filename + '.wav'
        # init variables
        extracted_features = {}  # init dictionary of extracted features
        audio_file_path = os.path.join('media', 'audio', audio_filename)  # audio file path
        mfccs_fig = Figure(facecolor=bg_color)  # init figure container
        mfccs_ax = mfccs_fig.subplots()  # init single plot container
        y, sr = librosa.load(audio_file_path, sr=sr)  # load audio file
        # print('librosa loaded audio file length: ', len(y))
        S, phase = librosa.magphase(librosa.stft(y=y, n_fft=spectral_parameters['nFFT'],
                                                 window=spectral_parameters['windowType'],
                                                 win_length=spectral_parameters['winLength'],
                                                 hop_length=spectral_parameters[
                                                     'hopLength']))  # extract magnitude and phase

        # S, phase = librosa.magphase(librosa.stft(y=y))  # extract magnitude and phase
        # MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr,
                                     n_mfcc=spectral_parameters['nMFCC'],
                                     n_fft=spectral_parameters['nFFT'],
                                     window=spectral_parameters['windowType'],
                                     win_length=spectral_parameters['winLength'],
                                     hop_length=spectral_parameters['hopLength'])  # extract mfccs
        # mfccs = librosa.feature.mfcc(y=y, sr=sr)
        mfccs_img = librosa.display.specshow(mfccs, sr=sr, x_axis='time', ax=mfccs_ax)  # create img for mfccs
        mfccs_fig.colorbar(mfccs_img, ax=mfccs_ax)
        mfccs_ax.set(title='MFCCs')
        # mfccs_ax.set_facecolor('yellow')
        extracted_features['mfccs'] = cls.save_feature_plot(mfccs_fig, 'mfccs', base_filename, plot_version_index)

        # Spectral centroid
        # cent = librosa.feature.spectral_centroid(y=y, sr=sr)  # extract spectral centroid
        centroid_fig = Figure(facecolor=bg_color)  # init figure container
        centroid_ax = centroid_fig.subplots()  # init single plot container
        # centroid = librosa.feature.spectral_centroid(S=S, sr=sr)
        centroid = librosa.feature.spectral_centroid(S=S,
                                                     sr=sr,
                                                     n_fft=spectral_parameters['nFFT'],
                                                     window=spectral_parameters['windowType'],
                                                     win_length=spectral_parameters['winLength'],
                                                     hop_length=spectral_parameters['hopLength']
                                                     )
        cent_times = librosa.times_like(centroid, sr=sr)  # extract times
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), sr=sr, y_axis='log', x_axis='time',
                                 ax=centroid_ax)
        centroid_ax.plot(cent_times, centroid.T, label='Spectral centroid', color='w')
        centroid_ax.legend(loc='upper right')
        centroid_ax.set(title='log Power spectrogram')
        extracted_features['spectralCentroid'] = cls.save_feature_plot(centroid_fig, 'spectralCentroid', base_filename, plot_version_index)

        # Spectral bandwidth
        spec_bw_fig = Figure(facecolor=bg_color)
        spec_bw_ax = spec_bw_fig.subplots()
        # spectral_bw = librosa.feature.spectral_bandwidth(S=S, sr=sr)
        spectral_bw = librosa.feature.spectral_bandwidth(S=S,
                                                         sr=sr,
                                                         n_fft=spectral_parameters['nFFT'],
                                                         window=spectral_parameters['windowType'],
                                                         win_length=spectral_parameters['winLength'],
                                                         hop_length=spectral_parameters['hopLength']
                                                         )
        spec_bw_times = librosa.times_like(spectral_bw, sr=sr)
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), sr=sr, y_axis='log', x_axis='time',
                                 ax=spec_bw_ax)
        # spec_bw_ax.set(title='Spectral bandwidth')
        spec_bw_ax.fill_between(spec_bw_times, np.maximum(0, centroid[0] - spectral_bw[0]),
                                np.minimum(centroid[0] + spectral_bw[0], sr / 2), alpha=0.5,
                                label='Centroid  +- bandwidth')
        spec_bw_ax.plot(spec_bw_times, centroid[0], label='Spectral centroid', color='w')
        spec_bw_ax.legend(loc='lower right')
        extracted_features['spectralBandwidth'] = cls.save_feature_plot(spec_bw_fig, 'spectralBandwidth', base_filename, plot_version_index)

        # Spectral contrast
        contrast_fig = Figure(facecolor=bg_color)
        contrast_ax = contrast_fig.subplots()
        # spectral_contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
        spectral_contrast = librosa.feature.spectral_contrast(S=S,
                                                              sr=sr,
                                                              n_fft=spectral_parameters['nFFT'],
                                                              window=spectral_parameters['windowType'],
                                                              win_length=spectral_parameters['winLength'],
                                                              hop_length=spectral_parameters['hopLength'],
                                                              fmin=spectral_parameters['contrastMinFreqCutoff'],
                                                              n_bands=spectral_parameters['contrastNumBands'],
                                                              )
        contrast_img = librosa.display.specshow(spectral_contrast, sr=sr, x_axis='time', ax=contrast_ax)
        contrast_fig.colorbar(contrast_img, ax=contrast_ax)
        contrast_ax.set(ylabel='Frequency bands', title='Spectral contrast')
        extracted_features['spectralContrast'] = cls.save_feature_plot(contrast_fig, 'spectralContrast', base_filename, plot_version_index)

        # Spectral roll-off
        rolloff_fig = Figure(facecolor=bg_color)
        rolloff_ax = rolloff_fig.subplots()
        # spectral_rolloff = librosa.feature.spectral_rolloff(S=S, sr=sr, roll_percent=0.85)
        spectral_rolloff = librosa.feature.spectral_rolloff(S=S,
                                                            sr=sr,
                                                            roll_percent=spectral_parameters['rollPercent'],
                                                            n_fft=spectral_parameters['nFFT'],
                                                            window=spectral_parameters['windowType'],
                                                            win_length=spectral_parameters['winLength'],
                                                            hop_length=spectral_parameters['hopLength']
                                                            )
        # rolloff_min = librosa.feature.spectral_rolloff(S=S, sr=sr, roll_percent=0.01)
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), sr=sr, y_axis='log', x_axis='time',
                                 ax=rolloff_ax)
        rolloff_ax.plot(librosa.times_like(spectral_rolloff, sr=sr), spectral_rolloff[0],
                        label='Roll-off frequency (0.85)')
        # rolloff_ax.plot(librosa.times_like(spectral_rolloff, sr=sr), rolloff_min[0], color='w',
        #                 label='Roll-off frequency (0.01)')
        rolloff_ax.legend(loc='upper right')
        rolloff_ax.set(title='Spectral Roll-off on log power spectrogram')
        extracted_features['spectralRollOff'] = cls.save_feature_plot(rolloff_fig, 'spectralRollOff', base_filename, plot_version_index)

        # Tonnetz
        # NOTA: tonnetz tira un warning sulla n_fft
        tonnetz_fig = Figure(facecolor=bg_color)
        tonnetz_ax = tonnetz_fig.subplots()
        harmonic_component = librosa.effects.harmonic(y)
        tonnetz = librosa.feature.tonnetz(y=harmonic_component, sr=sr)
        tonnetz_img = librosa.display.specshow(tonnetz, sr=sr, y_axis='tonnetz', x_axis='time', ax=tonnetz_ax)
        tonnetz_ax.set(title='Tonal centroids (Tonnetz)')
        tonnetz_fig.colorbar(tonnetz_img)
        extracted_features['tonnetz'] = cls.save_feature_plot(tonnetz_fig, 'tonnetz', base_filename, plot_version_index)
        return extracted_features

    @staticmethod
    def save_feature_plot(fig, feature_name, base_filename, plot_version_index) -> str:
        """
        Saves the feature plot to a file
        :param fig:
        :param feature_name:
        :param base_filename:
        :param plot_version_index:
        :return: filename: filename of the saved plot
        """
        filename = feature_name + '-' + base_filename + '-' + str(plot_version_index) + '.png'
        fig.savefig(os.path.join('media', 'images', filename), format="png")
        return filename

    @staticmethod
    def clear_old_plots(base_filename: str):
        """
        Clears old plot files
        :param base_filename:
        :return:
        """
        # old_plot_index = plot_version_index - 1
        files = glob.glob(os.path.join('media', 'images', '*' + base_filename + '*'))
        print('old plot files to be deleted: ', files)
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    # @staticmethod
    # def update_base_filename(base_filename: str) -> str:
    #     """
    #     Updates the base filename to the next progressive index to allow image refreshing
    #     :param base_filename:
    #     :return: updated_base_filename: the updated base filename
    #     """
    #     # First clear old plot files
    #     files = glob.glob(os.path.join('media', 'images', '*' + base_filename + '*'))
    #     for file in files:
    #         if os.path.exists(file):
    #             os.remove(file)
    #     print('retrieved files: ', files)
    #     # separator_occurrences = base_filename.count('-')
    #     # if separator_occurrences > 3:
    #     name = base_filename.split('-')
    #     progressive_index = int(name[len(name)-1]) + 1  # increase the progressive index of the image
    #     return '-'.join(name[0:len(name)-1]) + '-' + str(progressive_index)



