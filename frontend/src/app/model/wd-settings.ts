export interface WDParam {
    name: string;
    value: number;
    min: number;
    max: number;
    unit: string;
}

export class WDParamsContainer {
    private iterations: SimpleWDParam = {value: 88200, min: 1, max: 200000, unit: 'steps'};
}

export const WDPARAMETERS: Map<string, WDParam> = new Map<string, WDParam>();

export interface SimpleWDParam {
    value: number;
    min: number;
    max: number;
    unit: string;
}

// TODO add step to define granularity and decimals
// NOTE: default params refer to C4 note, unwrapped string
export const WDPARAMS: WDParam[] = [
    { name: 'iterations', value: 88200, min: 1, max: 200000, unit: 'steps' },
    { name: 'samplingFrequency', value: 44100, min: 1, max: 200000, unit: 'Hz' },
    { name: 'soundSpeed', value: 331, min: 300, max: 400, unit: 'm/s'},  // in m/s
    { name: 'stringFundamentalFrequency', value: 262.22, min: 20, max: 20000, unit: 'Hz' },
    { name: 'stringLength', value: 65.7, min: 5, max: 500, unit: 'cm' },
    { name: 'stringDiameter', value: 1.064, min: 0.5, max: 2, unit: 'mm' },
    { name: 'stringTension', value: 670, min: 400, max: 1000, unit: 'N' },
    { name: 'soundboardReflectionCoefficient', value: 98, min: 0, max: 100, unit: '%' },
    { name: 'hammerMass', value: 8.71, min: 5, max: 11, unit: 'g' },
    { name: 'hammerRelativeStrikingPoint', value: 0.116, min: 0, max: 1, unit: '%' },
    { name: 'hammerInitialVelocity', value: 7, min: 0, max: 10, unit: 'm/s' },
    { name: 'hammerStringDistance', value: 10, min: 0, max: 30, unit: 'cm' },
    { name: 'linearFeltStiffness', value: 1000, min: 0, max: 10000, unit: 'N/m' },
]

// export class WDParameters {
//     /**
//      * This class represents the simulation parameters to be sent to the server.
//      * 
//      * @param iterations - the number of iterations to be performed
//      * @samplingFrequency - the sampling frequency of the simulation in Hz
//      * @param stringFrequency - the fundamental frequency of the string in Hz
//      * @param soundSpeed - the speed of sound in m/s
//      * @param stringTension - the tension of the string at rest in N
//      * @param stringLength - the length of the string in cm
//      * @param stringDiameter - the diameter of the string in mm
//      * @param soundboardReflectionCoefficient - the reflection coefficient of the soundboard
//      * @param hammerMass - the mass of the hammer in g
//      * @param linearFeltStiffness - the linear stiffness of the felt in N/m
//      * @param hammerRelativeStrikingPoint - the relative striking point of the hammer in % 
//      * @param hammerInitialVelocity - the initial velocity of the hammer in m/s
//      * @param hammerStringDistance - the distance between the hammer and the string in cm
//      */
//     private iterations: WDParam = { value: 88200, min: 1, max: 200000 };
//     private samplingFrequency: WDParam = {value: 44100, min: 1, max: 200000};
//     private soundSpeed: WDParam = {value: 331, min: 300, max: 400};  // in m/s
//     private stringFrequency: WDParam = { value: 262.22, min: 20, max: 20000 };
//     private stringTension: WDParam = { value: 670, min: 400, max: 1000 };
//     private stringLength: WDParam = { value: 65.7, min: 5, max: 500 };
//     private stringDiameter: WDParam = { value: 1.064, min: 0.5, max: 2 };
//     private soundboardReflectionCoefficient: WDParam = { value: 0.98, min: 0, max: 1 };
//     private hammerMass: WDParam = { value: 8.71, min: 5, max: 10 };
//     private hammerRelativeStrikingPoint: WDParam = { value: 0.116, min: 0, max: 1 };
//     private hamerInitialVelocity: WDParam = { value: 7, min: 0, max: 10 };
//     private hammerStringDistance: WDParam = { value: 0.01, min: 0, max: 30 };
//     private linearFeltStiffness: WDParam = { value: 1000, min: 0, max: 10000 };

//     // constructor(iterations: number,
//     //     samplingFrequency: number,
//     //     soundSpeed: number,
//     //     stringFrequency: number,
//     //     stringTension: number,
//     //     stringLength: number,
//     //     stringDiameter: number,
//     //     soundboardReflectionCoefficient: number,
//     //     hammerMass: number,
//     //     hammerRelativeStrikingPoint: number,
//     //     hammerInitialVelocity: number,
//     //     hammerStringDistance: number,
//     //     linearFeltStiffness: number) {
//     //     this.iterations.value = iterations;
//     //     this.samplingFrequency = samplingFrequency;
//     //     this.soundSpeed = soundSpeed;
//     //     this.stringFrequency.value = stringFrequency;
//     //     this.stringTension.value = stringTension;
//     //     this.stringLength.value = stringLength;
//     //     this.stringDiameter.value = stringDiameter;
//     //     this.soundboardReflectionCoefficient.value = soundboardReflectionCoefficient;
//     //     this.hammerMass.value = hammerMass;
//     //     this.hammerRelativeStrikingPoint.value = hammerRelativeStrikingPoint;
//     //     this.hamerInitialVelocity.value = hammerInitialVelocity;
//     //     this.hammerStringDistance.value = hammerStringDistance;
//     //     this.linearFeltStiffness.value = linearFeltStiffness;
//     // }
//     constructor() { }

//     public getIterations(): WDParam {
//         return this.iterations;
//     }

//     public getSamplingFrequency(): WDParam {
//         return this.samplingFrequency;
//     }

//     public getSoundSpeed(): WDParam {
//         return this.soundSpeed;
//     }

//     public getStringFrequency(): WDParam {
//         return this.stringFrequency
//     }

//     public getStringTension(): WDParam {
//         return this.stringTension
//     }

//     public getStringLength(): WDParam {
//         return this.stringLength;
//     }

//     public getStringDiameter(): WDParam {
//         return this.stringDiameter;
//     }

//     public getSoundboardReflectionCoefficient(): WDParam {
//         return this.soundboardReflectionCoefficient;
//     }

//     public getHammerMass(): WDParam {
//         return this.hammerMass;
//     }

//     public getLinearFeltStiffness(): WDParam {
//         return this.linearFeltStiffness;
//     }

//     public getHammerRelativeStrikingPoint(): WDParam {
//         return this.hammerRelativeStrikingPoint;
//     }

//     public getHammerInitialVelocity(): WDParam {
//         return this.hamerInitialVelocity;
//     }

//     public getHammerStringDistance(): WDParam {
//         return this.hammerStringDistance;
//     }
// }

// export class WDBounds {
//     /**
//      * this class defines the bounds for the parameters of the simulation
//      */
//     private iterations = { min: 1000, max: 200000 };
//     private stringFrequency = {min: 20, max:20000}; // in Hz
//     private stringTension = {min : 400, max: 1000}; // in N
//     private stringLength = {min: 5, max: 500}; // in cm
//     private stringDiameter = {min: 0.5, max: 2}; // in mm
//     private soundboardReflectionCoefficient = {min: 0, max: 1};
//     private hammerMass = {min: 5, max: 10}; // in g
//     private linearFeltStiffness = {min: 0, max: 10000}; // in N/m
//     private hammerInitialVelocity = {min: 0, max: 10}; // in m/s
//     private hammerRelativeStrikingPoint = {min: 0, max: 1}; // in %
//     private hammerStringDistance = {min: 0, max: 30}; // in cm

//     public getIterations(): any {
//         return this.iterations;
//     }

//     public getStringFrequency(): any {
//         return this.stringFrequency;
//     }

//     public getStringTension(): any {
//         return this.stringTension;
//     }

//     public getStringLength(): any {
//         return this.stringLength;
//     }

//     public getStringDiameter(): any {
//         return this.stringDiameter;
//     }

//     public getSoundboardReflectionCoefficient(): any {
//         return this.soundboardReflectionCoefficient;
//     }

//     public getHammerMass(): any {
//         return this.hammerMass;
//     }

//     public getLinearFeltStiffness(): any {
//         return this.linearFeltStiffness;
//     }

//     public getHammerInitialVelocity(): any {
//         return this.hammerInitialVelocity;
//     }

//     public getHammerRelativeStrikingPoint(): any {
//         return this.hammerRelativeStrikingPoint;
//     }

//     public getHammerStringDistance(): any {
//         return this.hammerStringDistance;
//     }
// }