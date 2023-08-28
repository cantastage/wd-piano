#  Feature richieste: MFCCs, spectral centroid, spectral roll-off, spectral bandwidth, tonnetz, etc.
import os
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

    # TODO add all the requested features and return dictionary with names so it is easily jsonified
    @classmethod
    def extract_features(cls, audio_file_name):
        """
        Extracts the features from the audio file
        :param audio_file_name: the audio file
        :return: the extracted features
        """
        # init variables
        extracted_features = {}  # init dictionary of extracted features
        audio_file_path = os.path.join('media', 'audio', audio_file_name) # audio file path
        mfccs_fig = Figure()  # init figure container
        mfccs_ax = mfccs_fig.subplots()  # init single plot container
        y, sr = librosa.load(audio_file_path, sr=Settings.get_sampling_freq())  # load audio file
        S, phase = librosa.magphase(librosa.stft(y=y))  # extract magnitude and phase

        # MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr)  # extract mfccs
        mfccs_img = librosa.display.specshow(mfccs, x_axis='time', ax=mfccs_ax)  # create img for mfccs
        mfccs_fig.colorbar(mfccs_img, ax=mfccs_ax)
        mfccs_ax.set(title='MFCCs')
        extracted_features['mfccs'] = cls.save_feature_plot(mfccs_fig, 'mfccs', Settings.get_base_filename())

        # Spectral centroid
        # cent = librosa.feature.spectral_centroid(y=y, sr=sr)  # extract spectral centroid
        centroid_fig = Figure()  # init figure container
        centroid_ax = centroid_fig.subplots()  # init single plot container
        centroid = librosa.feature.spectral_centroid(S=S)
        cent_times = librosa.times_like(centroid)  # extract times
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=centroid_ax)
        centroid_ax.plot(cent_times, centroid.T, label='Spectral centroid', color='w')
        centroid_ax.legend(loc='upper right')
        centroid_ax.set(title='log Power spectrogram')
        extracted_features['spectralCentroid'] = cls.save_feature_plot(centroid_fig, 'spectralCentroid', Settings.get_base_filename())

        spec_bw_fig = Figure()
        spec_bw_ax = spec_bw_fig.subplots()
        spectral_bw = librosa.feature.spectral_bandwidth(S=S)
        spec_bw_times = librosa.times_like(spectral_bw)
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=spec_bw_ax)
        spec_bw_ax.fill_between(spec_bw_times, np.maximum(0, centroid[0] - spectral_bw[0]), np.minimum(centroid[0] + spectral_bw[0], sr/2), alpha=0.5, label='Centroid  +- bandwidth')
        spec_bw_ax.plot(spec_bw_times, centroid[0], label='Spectral centroid', color='w')
        spec_bw_ax.legend(loc='lower right')
        extracted_features['spectralBandwidth'] = cls.save_feature_plot(spec_bw_fig, 'spectralBandwidth', Settings.get_base_filename())

        return extracted_features
        # fig.savefig(os.path.join('media', 'images', plot_filename), format="png")

    @staticmethod
    def save_feature_plot(fig, feature_name, base_filename) -> str:
        """
        Saves the feature plot to a file
        :param fig:
        :param feature_name:
        :param base_filename:
        :return: filename: filename of the saved plot
        """
        filename = feature_name + '-' + base_filename + '.png'
        fig.savefig(os.path.join('media', 'images', filename), format="png")
        return filename