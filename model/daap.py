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
    def extract_features(cls, base_filename: str, spectral_parameters: dict, plot_version_index: int) -> dict:
        """
        Extracts spectral features from the audio file
        :param base_filename: base filename to retrieve audio data and plots data
        :param spectral_parameters: the parameters for the extraction of the spectral features
        :param plot_version_index: progressive index of plot versions
        :return: the extracted features
        """
        print('Starting extraction of spectral features...')
        bg_color = '#f2f2f2'
        # print('Arrived spectral parameters: ', spectral_parameters)
        if plot_version_index > 0:
            cls.clear_old_plots(base_filename)  # clear old plot files
        sr = Settings.get_sampling_freq()
        # Extract spectral analysis parameters
        n_fft = spectral_parameters['nFFT']
        window_type = spectral_parameters['windowType']
        win_length = spectral_parameters['winLength']
        hop_length = spectral_parameters['hopLength']
        audio_filename = base_filename + '.wav'
        # init variables
        extracted_features = {}  # init dictionary of extracted features
        audio_file_path = os.path.join('media', 'audio', audio_filename)  # audio file path

        y, sr = librosa.load(audio_file_path, sr=sr)  # load audio file

        # print('librosa loaded audio file length: ', len(y))
        S, phase = librosa.magphase(librosa.stft(y=y,
                                                 n_fft=n_fft,
                                                 window=window_type,
                                                 win_length=win_length,
                                                 hop_length=hop_length,
                                                 center=False))  # extract magnitude and phase

        # MFCCs
        mfccs_fig = Figure(facecolor=bg_color)  # init figure container
        mfccs_ax = mfccs_fig.subplots()  # init single plot container
        mfccs = librosa.feature.mfcc(y=y, sr=sr,
                                     n_mfcc=spectral_parameters['nMFCC'],
                                     n_fft=n_fft,
                                     window=window_type,
                                     win_length=win_length,
                                     hop_length=hop_length)  # extract mfccs
        # NOTE: We remove first MFCCs coefficient for better viewing
        modified_mfccs = np.delete(mfccs, 0, axis=0)
        mfccs_img = librosa.display.specshow(modified_mfccs,
                                             sr=sr,
                                             hop_length=hop_length,
                                             x_axis='time',
                                             y_axis='mel',
                                             ax=mfccs_ax)  # create img for mfccs
        mfccs_fig.colorbar(mfccs_img, ax=mfccs_ax)
        mfccs_ax.set(title='MFCCs')
        extracted_features['mfccs'] = cls.save_feature_plot(mfccs_fig, 'mfccs', base_filename, plot_version_index)

        # Spectral centroid
        centroid_fig = Figure(facecolor=bg_color)  # init figure container
        centroid_ax = centroid_fig.subplots()  # init single plot container
        centroid = librosa.feature.spectral_centroid(S=S,
                                                     sr=sr,
                                                     n_fft=n_fft,
                                                     window=window_type,
                                                     win_length=win_length,
                                                     hop_length=hop_length,
                                                     )
        cent_times = librosa.times_like(centroid, sr=sr, hop_length=hop_length)  # extract times
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                                 sr=sr,
                                 hop_length=hop_length,
                                 y_axis='log',
                                 x_axis='time',
                                 ax=centroid_ax)
        centroid_ax.plot(cent_times, centroid.T, label='Spectral centroid', color='w')
        centroid_ax.legend(loc='upper right')
        centroid_ax.set(title='Spectral centroid on log-power spectrogram')
        extracted_features['spectralCentroid'] = cls.save_feature_plot(centroid_fig,
                                                                       'spectralCentroid',
                                                                       base_filename,
                                                                       plot_version_index)

        # Spectral bandwidth
        spec_bw_fig = Figure(facecolor=bg_color)
        spec_bw_ax = spec_bw_fig.subplots()
        spectral_bw = librosa.feature.spectral_bandwidth(S=S,
                                                         sr=sr,
                                                         n_fft=n_fft,
                                                         window=window_type,
                                                         win_length=win_length,
                                                         hop_length=hop_length)
        spec_bw_times = librosa.times_like(spectral_bw, sr=sr, hop_length=hop_length)
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                                 sr=sr,
                                 hop_length=hop_length,
                                 y_axis='log',
                                 x_axis='time',
                                 ax=spec_bw_ax)
        spec_bw_ax.fill_between(spec_bw_times, np.maximum(0, centroid[0] - spectral_bw[0]),
                                np.minimum(centroid[0] + spectral_bw[0], sr / 2), alpha=0.5,
                                label='Centroid  +- bandwidth')
        spec_bw_ax.plot(spec_bw_times, centroid[0], label='Spectral centroid', color='w')
        spec_bw_ax.legend(loc='lower right')
        spec_bw_ax.set(title='Spectral bandwidth on log-power spectrogram')
        extracted_features['spectralBandwidth'] = cls.save_feature_plot(spec_bw_fig, 'spectralBandwidth', base_filename, plot_version_index)

        # Spectral contrast
        contrast_fig = Figure(facecolor=bg_color)
        contrast_ax = contrast_fig.subplots()
        spectral_contrast = librosa.feature.spectral_contrast(S=S,
                                                              sr=sr,
                                                              n_fft=n_fft,
                                                              window=window_type,
                                                              win_length=win_length,
                                                              hop_length=hop_length,
                                                              fmin=spectral_parameters['contrastMinFreqCutoff'],
                                                              n_bands=spectral_parameters['contrastNumBands'],
                                                              )
        contrast_img = librosa.display.specshow(spectral_contrast,
                                                sr=sr,
                                                hop_length=hop_length,
                                                x_axis='time',
                                                ax=contrast_ax)
        contrast_fig.colorbar(contrast_img, ax=contrast_ax)
        contrast_ax.set(ylabel='Frequency bands', title='Spectral contrast')
        extracted_features['spectralContrast'] = cls.save_feature_plot(contrast_fig,
                                                                       'spectralContrast',
                                                                       base_filename,
                                                                       plot_version_index)

        # Spectral roll-off
        rolloff_fig = Figure(facecolor=bg_color)
        rolloff_ax = rolloff_fig.subplots()
        # spectral_rolloff = librosa.feature.spectral_rolloff(S=S, sr=sr, roll_percent=0.85)
        spectral_rolloff = librosa.feature.spectral_rolloff(S=S,
                                                            sr=sr,
                                                            roll_percent=spectral_parameters['rollPercent'],
                                                            n_fft=n_fft,
                                                            window=window_type,
                                                            win_length=win_length,
                                                            hop_length=hop_length)
        # rolloff_min = librosa.feature.spectral_rolloff(S=S, sr=sr, roll_percent=0.01)
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                                 sr=sr,
                                 hop_length=hop_length,
                                 y_axis='log',
                                 x_axis='time',
                                 ax=rolloff_ax)
        rolloff_ax.plot(librosa.times_like(spectral_rolloff, sr=sr, hop_length=hop_length), spectral_rolloff[0],
                        label='Roll-off frequency (0.85)')
        rolloff_ax.legend(loc='upper right')
        rolloff_ax.set(title='Spectral Roll-off on log power spectrogram')
        extracted_features['spectralRollOff'] = cls.save_feature_plot(rolloff_fig,
                                                                      'spectralRollOff',
                                                                      base_filename,
                                                                      plot_version_index)

        # Tonnetz
        # NOTA: tonnetz tira un warning sulla n_fft
        tonnetz_fig = Figure(facecolor=bg_color)
        tonnetz_ax = tonnetz_fig.subplots()
        harmonic_component = librosa.effects.harmonic(y)
        tonnetz = librosa.feature.tonnetz(y=harmonic_component, sr=sr)
        tonnetz_img = librosa.display.specshow(tonnetz, sr=sr, y_axis='tonnetz', x_axis='time', ax=tonnetz_ax)
        tonnetz_ax.set(title='Tonal centroids (Tonnetz)')
        tonnetz_fig.colorbar(tonnetz_img)
        extracted_features['tonnetz'] = cls.save_feature_plot(tonnetz_fig,
                                                              'tonnetz',
                                                              base_filename,
                                                              plot_version_index)
        print('Finished extraction of spectral features')
        return extracted_features

    # @classmethod
    # def batch_extract_features(cls,
    #                            base_filename: str,
    #                            audio_base_filenames: list[str],
    #                            spectral_parameters: dict,
    #                            plot_version_index: int) -> dict:
    #     print('Starting comparing spectral features...')
    #     num_files = len(audio_base_filenames)
    #     bg_color = '#f2f2f2'
    #     # print('Arrived spectral parameters: ', spectral_parameters)
    #     if plot_version_index > 0:
    #         cls.clear_old_plots(base_filename)  # clear old plot files
    #     sr = Settings.get_sampling_freq()
    #     # Extract spectral analysis parameters
    #     n_fft = spectral_parameters['nFFT']
    #     window_type = spectral_parameters['windowType']
    #     win_length = spectral_parameters['winLength']
    #     hop_length = spectral_parameters['hopLength']
    #
    #     # init matplotlib figures
    #     mfccs_fig = Figure(facecolor=bg_color)  # init figure container
    #     mfccs_ax = mfccs_fig.subplots(nrows=1, ncols=num_files).flatten()  # init single plot container
    #
    #     centroid_fig = Figure(facecolor=bg_color)  # init figure container
    #     centroid_ax = centroid_fig.subplots(nrows=1, ncols=num_files).flatten()  # init single plot container
    #
    #     spec_bw_fig = Figure(facecolor=bg_color)
    #     spec_bw_ax = spec_bw_fig.subplots(nrows=1, ncols=num_files).flatten()
    #
    #     contrast_fig = Figure(facecolor=bg_color)
    #     contrast_ax = contrast_fig.subplots(nrows=1,ncols=num_files).flatten()
    #
    #     rolloff_fig = Figure(facecolor=bg_color)
    #     rolloff_ax = rolloff_fig.subplots(nrows=1, ncols=num_files).flatten()
    #
    #     tonnetz_fig = Figure(facecolor=bg_color)
    #     tonnetz_ax = tonnetz_fig.subplots(nrows=1, ncols=num_files).flatten()
    #
    #     # init variables
    #     extracted_features = {}  # init dictionary of extracted features
    #     for i in range(0, len(audio_base_filenames)):
    #         audio_file_path = os.path.join('media', 'audio', audio_base_filenames[i] + '.wav')  # audio file path
    #         y, sr = librosa.load(audio_file_path, sr=sr)  # load audio file
    #
    #         S, phase = librosa.magphase(librosa.stft(y=y,
    #                                                  n_fft=n_fft,
    #                                                  window=window_type,
    #                                                  win_length=win_length,
    #                                                  hop_length=hop_length,
    #                                                  center=False))  # extract magnitude and phase
    #
    #         # MFCCs
    #         # mfccs_fig = Figure(facecolor=bg_color)  # init figure container
    #         # mfccs_ax = mfccs_fig.subplots()  # init single plot container
    #         mfccs = librosa.feature.mfcc(y=y, sr=sr,
    #                                      n_mfcc=spectral_parameters['nMFCC'],
    #                                      n_fft=n_fft,
    #                                      window=window_type,
    #                                      win_length=win_length,
    #                                      hop_length=hop_length)  # extract mfccs
    #         mfccs_img = librosa.display.specshow(mfccs,
    #                                              sr=sr,
    #                                              hop_length=hop_length,
    #                                              x_axis='time',
    #                                              ax=mfccs_ax[i])  # create img for mfccs
    #         mfccs_fig.colorbar(mfccs_img, ax=mfccs_ax)
    #         mfccs_ax[i].set(title='MFCCs')
    #         extracted_features['mfccs'] = cls.save_feature_plot(mfccs_fig, 'mfccs', base_filename, plot_version_index)
    #
    #         # Spectral centroid
    #         # centroid_fig = Figure(facecolor=bg_color)  # init figure container
    #         # centroid_ax = centroid_fig.subplots()  # init single plot container
    #         centroid = librosa.feature.spectral_centroid(S=S,
    #                                                      sr=sr,
    #                                                      n_fft=n_fft,
    #                                                      window=window_type,
    #                                                      win_length=win_length,
    #                                                      hop_length=hop_length,
    #                                                      )
    #         cent_times = librosa.times_like(centroid, sr=sr, hop_length=hop_length)  # extract times
    #         librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
    #                                  sr=sr,
    #                                  hop_length=hop_length,
    #                                  y_axis='log',
    #                                  x_axis='time',
    #                                  ax=centroid_ax[i])
    #         centroid_ax[i].plot(cent_times, centroid.T, label='Spectral centroid', color='w')
    #         centroid_ax[i].legend(loc='upper right')
    #         centroid_ax[i].set(title='Spectral centroid on log-power spectrogram')
    #         extracted_features['spectralCentroid'] = cls.save_feature_plot(centroid_fig,
    #                                                                        'spectralCentroid',
    #                                                                        base_filename,
    #                                                                        plot_version_index)
    #
    #         # Spectral bandwidth
    #         # spec_bw_fig = Figure(facecolor=bg_color)
    #         # spec_bw_ax = spec_bw_fig.subplots()
    #         spectral_bw = librosa.feature.spectral_bandwidth(S=S,
    #                                                          sr=sr,
    #                                                          n_fft=n_fft,
    #                                                          window=window_type,
    #                                                          win_length=win_length,
    #                                                          hop_length=hop_length)
    #         spec_bw_times = librosa.times_like(spectral_bw, sr=sr, hop_length=hop_length)
    #         librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
    #                                  sr=sr,
    #                                  hop_length=hop_length,
    #                                  y_axis='log',
    #                                  x_axis='time',
    #                                  ax=spec_bw_ax[i])
    #         spec_bw_ax[i].fill_between(spec_bw_times, np.maximum(0, centroid[0] - spectral_bw[0]),
    #                                 np.minimum(centroid[0] + spectral_bw[0], sr / 2), alpha=0.5,
    #                                 label='Centroid  +- bandwidth')
    #         spec_bw_ax[i].plot(spec_bw_times, centroid[0], label='Spectral centroid', color='w')
    #         spec_bw_ax[i].legend(loc='lower right')
    #         spec_bw_ax[i].set(title='Spectral bandwidth on log-power spectrogram')
    #         extracted_features['spectralBandwidth'] = cls.save_feature_plot(spec_bw_fig, 'spectralBandwidth', base_filename,
    #                                                                         plot_version_index)
    #
    #         # Spectral contrast
    #         # contrast_fig = Figure(facecolor=bg_color)
    #         # contrast_ax = contrast_fig.subplots()
    #         spectral_contrast = librosa.feature.spectral_contrast(S=S,
    #                                                               sr=sr,
    #                                                               n_fft=n_fft,
    #                                                               window=window_type,
    #                                                               win_length=win_length,
    #                                                               hop_length=hop_length,
    #                                                               fmin=spectral_parameters['contrastMinFreqCutoff'],
    #                                                               n_bands=spectral_parameters['contrastNumBands'],
    #                                                               )
    #         contrast_img = librosa.display.specshow(spectral_contrast,
    #                                                 sr=sr,
    #                                                 hop_length=hop_length,
    #                                                 x_axis='time',
    #                                                 ax=contrast_ax[i])
    #         contrast_fig.colorbar(contrast_img, ax=contrast_ax)
    #         contrast_ax[i].set(ylabel='Frequency bands', title='Spectral contrast')
    #         extracted_features['spectralContrast'] = cls.save_feature_plot(contrast_fig,
    #                                                                        'spectralContrast',
    #                                                                        base_filename,
    #                                                                        plot_version_index)
    #
    #         # Spectral roll-off
    #         # rolloff_fig = Figure(facecolor=bg_color)
    #         # rolloff_ax = rolloff_fig.subplots()
    #         # spectral_rolloff = librosa.feature.spectral_rolloff(S=S, sr=sr, roll_percent=0.85)
    #         spectral_rolloff = librosa.feature.spectral_rolloff(S=S,
    #                                                             sr=sr,
    #                                                             roll_percent=spectral_parameters['rollPercent'],
    #                                                             n_fft=n_fft,
    #                                                             window=window_type,
    #                                                             win_length=win_length,
    #                                                             hop_length=hop_length)
    #         # rolloff_min = librosa.feature.spectral_rolloff(S=S, sr=sr, roll_percent=0.01)
    #         librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
    #                                  sr=sr,
    #                                  hop_length=hop_length,
    #                                  y_axis='log',
    #                                  x_axis='time',
    #                                  ax=rolloff_ax[i])
    #         rolloff_ax[i].plot(librosa.times_like(spectral_rolloff, sr=sr, hop_length=hop_length), spectral_rolloff[0],
    #                         label='Roll-off frequency (0.85)')
    #         rolloff_ax[i].legend(loc='upper right')
    #         rolloff_ax[i].set(title='Spectral Roll-off on log power spectrogram')
    #         extracted_features['spectralRollOff'] = cls.save_feature_plot(rolloff_fig,
    #                                                                       'spectralRollOff',
    #                                                                       base_filename,
    #                                                                       plot_version_index)
    #
    #         # Tonnetz
    #         # NOTA: tonnetz tira un warning sulla n_fft
    #         # tonnetz_fig = Figure(facecolor=bg_color)
    #         # tonnetz_ax = tonnetz_fig.subplots()
    #         harmonic_component = librosa.effects.harmonic(y)
    #         tonnetz = librosa.feature.tonnetz(y=harmonic_component, sr=sr)
    #         tonnetz_img = librosa.display.specshow(tonnetz, sr=sr, y_axis='tonnetz', x_axis='time', ax=tonnetz_ax[i])
    #         tonnetz_ax[i].set(title='Tonal centroids (Tonnetz)')
    #         tonnetz_fig.colorbar(tonnetz_img)
    #         extracted_features['tonnetz'] = cls.save_feature_plot(tonnetz_fig,
    #                                                               'tonnetz',
    #                                                               base_filename,
    #                                                               plot_version_index)
    #     print('Finished extraction of spectral features')
    #     return extracted_features





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




