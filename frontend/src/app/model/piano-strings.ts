// NOTE: we refer to notes from C1 to B7 because we have data for that strings only

/**
 * Class describing a piano string
 */
export class PianoKey  {
    private noteLabel: string; // e.g. "A4"
    private centerFrequency: number; // [Hz]
    private stringLength: number; // [m]
    private stringDiameter: number;  // [mm]
    private stringVolumetricDensity: number; // [kg/m^(-3)]
    private stringTension: number; // [N]

    private hammerNonLinearElasticExponent: number;
    private hammerImpactPosition: number; // [m]
    private hammerMass: number; // [g]
    private hammerElasticityCoefficient: number; // [N/m^-p]


    constructor(noteLabel: string,
        centerFrequency: number,
        stringLength: number,
        stringDiameter: number,
        stringVolumetricDensity: number,
        tension: number,
        hammerNonLinearElasticExponent: number,
        hammerImpactPosition: number,
        hammerMass: number,
        hammerElasticityCoefficient: number) {
        // super(); // TODO uncomment only if you want to extend Object class
        this.noteLabel = noteLabel;
        this.centerFrequency = centerFrequency;
        this.stringLength = stringLength;
        this.stringDiameter = stringDiameter;
        this.stringVolumetricDensity = stringVolumetricDensity;
        this.stringTension = tension;
        this.hammerNonLinearElasticExponent = hammerNonLinearElasticExponent;
        this.hammerImpactPosition = hammerImpactPosition;
        this.hammerMass = hammerMass;
        this.hammerElasticityCoefficient = hammerElasticityCoefficient;
    }

    getNoteLabel(): string {
        return this.noteLabel;
    }

    getCenterFrequency(): number {
        return this.centerFrequency;
    }

    getStringLength(): number {
        return this.stringLength;
    }

    getStringDiameter(): number {
        return this.stringDiameter;
    }

    getStringVolumetricDensity(): number {
        return this.stringVolumetricDensity;
    }

    getStringTension(): number {
        return this.stringTension;
    }

    getHammerNonLinearElasticExponent(): number {
        return this.hammerNonLinearElasticExponent;
    }

    getHammerImpactPosition(): number {
        return this.hammerImpactPosition;
    }

    getHammerMass(): number {
        return this.hammerMass;
    }

    getHammerElasticityCoefficient(): number {
        return this.hammerElasticityCoefficient;
    }
}

// export const unwrappedPianoStrings: UnwrappedPianoString[] = [

// ]

// export const center_frequencies: number[] = [
//     32.78,
//     34.73,
//     36.79,
//     38.98,
//     41.30,
//     43.75,
//     46.35,
//     49.11,
//     52.03,
//     55.12,
//     58.40,
//     61.87,
//     65.55,
//     69.45,
//     73.58,
//     77.96,
//     82.59,
//     87.51,
//     92.71,
//     98.22,
//     104.06,
//     110.25,
//     116.81,
//     123.75,
//     131,11,
//     138.90,
//     147.17,
//     155.91,
//     165.19,
//     175.01,
//     185.41,
//     196.45,
//     208.12,
//     220.49,
//     233.62,
//     247.52,
//     262.22,
//     277.81,
//     294.34,
//     311.82,
//     330.36,
//     350.05,
//     370.80,
//     392.87,
//     416.26,
//     441.01,
//     467.19,
//     494.96,
//     524.48,
//     555.60,
//     588.66,
//     623.69,
//     660.69,
//     699.91,
//     741.65,
//     785.63,
//     832.54,
//     882.06,
//     934.60,
//     990.20,
//     1048.83,
//     1111.06,
//     1177.66,
//     1247.25,
//     1321.31,
//     1399.97,
//     1483.31,
//     1571.35,
//     1665.41,
//     1764.21,
//     1869.22,
//     1980.57,
//     2098.32,
//     2222.39,
//     2355.34,
//     2494.63,
//     2643.17,
//     2801.35,
//     2965.15,
//     3142.89,
//     3330.76,
//     3528.57,
//     3735.94,
//     3959.63
// ]

// export const unwrappedStringLengths: number[] = [
// ]

// export const unwrappedStringDiameters: number[] = [
// ]

// export const unwrappedStringTensions: number[] = [