/**
 * Complete WDParam with min and max values
 */
export interface WDParam {
    name: string;
    value: number;
    min: number;
    max: number;
    unit: string;
}

// export const WDPARAMETERS: Map<string, WDParam> = new Map<string, WDParam>();

/**
 * Simple WDParam for summary description purposes
 */
export interface SimpleWDParam {
    value: number;
    unit: string;
}

// TODO add step to define granularity and decimals
// NOTE: default params refer to C4 note, unwrapped string
export const WDPARAMS: WDParam[] = [
    { name: 'iterations', value: 88200, min: 1, max: 200000, unit: 'steps' },
    { name: 'samplingFrequency', value: 44100, min: 1, max: 200000, unit: 'Hz' },
    { name: 'soundSpeed', value: 343.43, min: 300, max: 400, unit: 'm/s'},  // in m/s
    { name: 'stringFundamentalFrequency', value: 262.22, min: 20, max: 20000, unit: 'Hz' },
    { name: 'stringLength', value: 0.657, min: 0.05, max: 5.00, unit: 'm' },
    { name: 'stringDiameter', value: 1.064, min: 0.5, max: 2, unit: 'mm' },
    { name: 'stringTension', value: 829, min: 400, max: 1000, unit: 'N' },
    { name: 'soundboardReflectionCoefficient', value: 98, min: 0, max: 100, unit: '%' },
    { name: 'hammerMass', value: 8.71, min: 5, max: 11, unit: 'g' },
    { name: 'hammerRelativeStrikingPoint', value: 12, min: 0, max: 100, unit: '%' },
    { name: 'hammerInitialVelocity', value: 7, min: 0, max: 10, unit: 'm/s' },
    { name: 'hammerStringDistance', value: 10, min: 0, max: 30, unit: 'cm' },
    { name: 'linearFeltStiffness', value: 1000, min: 0, max: 10000, unit: 'N/m' },
];