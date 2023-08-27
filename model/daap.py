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
        y, sr = librosa.load(os.path.join('media', 'audio', audio_file_name), sr=Settings.get_sampling_freq())  # load audio file
        mfccs = librosa.feature.mfcc(y=y, sr=sr)  # extract mfccs
        fig = Figure()  # create figure container
        ax = fig.subplots()  # create single plot container
        img = librosa.display.specshow(mfccs, x_axis='time', ax=ax)  # create img for mfccs
        fig.colorbar(img, ax=ax)
        # ax.setTitle('MFCCs')
        # ax.label_outer()
        base_filename = Settings.get_base_filename()  # get base filename
        plot_filename = 'mfccs_' + base_filename + '.png'
        fig.savefig(os.path.join('media', 'images', plot_filename), format="png")
        return plot_filename

