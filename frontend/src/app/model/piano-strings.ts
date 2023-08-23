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