export interface SpectralFeatures {
    mfccs: string;
    spectralCentroid: string;
    spectralBandwidth: string;
    spectralContrast: string;
    spectralRollOff: string;
    tonnetz: string;
    // TODO add all other features when implemented
}

export interface SpectralAnalysisParameters {
    baseFilename: string;
    // "almost" common parameters
    nFFT: number;
    windowType: string;
    winLength: number;  // NOTE: has to be <= nFFT
    hopLength: number;

    // MFCC
    nMFCC: number;
    // Spectral Contrast
    contrastMinFreqCutoff: number;
    contrastNumBands: number; // > 1
    // Spectral Roll-off
    rollPercent: number;
}

export const DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS: SpectralAnalysisParameters = {
    baseFilename: '',
    nFFT: 2048,
    windowType: 'hann',
    winLength: 2048,
    hopLength: 512,
    nMFCC: 20,
    contrastMinFreqCutoff: 200.0,
    contrastNumBands: 6,
    rollPercent: 0.85
}