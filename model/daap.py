#  Feature richieste: MFCCs, spectral centroid, spectral roll-off, spectral bandwidth, tonnetz, etc.
import librosa
import os
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
        extracted_features = {}  # init dictionary of extracted features
        y, sr = librosa.load(os.path.join('media', 'audio', audio_file_name), sr=Settings.get_sampling_freq())  # load audio file
        fig = Figure()  # init figure container
        ax = fig.subplots()  # init single plot container
        # MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr)  # extract mfccs
        img = librosa.display.specshow(mfccs, x_axis='time', ax=ax)  # create img for mfccs
        fig.colorbar(img, ax=ax)
        ax.set(title='MFCCs')
        extracted_features['mfccs'] = cls.save_feature_plot(fig, 'mfccs', Settings.get_base_filename())  # save mfccs plot
        # Spectral centroid
        # cent = librosa.feature.spectral_centroid(y=y, sr=sr)  # extract spectral centroid
        S, phase = librosa.magphase(librosa.stft(y=y))  # extract magnitude and phase
        cent = librosa.feature.spectral_centroid(S=S)
        times = librosa.times_like(cent)  # extract times
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=ax)
        ax.plot(times, cent.T, label='Spectral centroid', color='w')
        ax.legend(loc='upper right')
        ax.set(title='log Power spectrogram')
        extracted_features['spectralCentroid'] = cls.save_feature_plot(fig, 'spectralCentroid', Settings.get_base_filename()
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