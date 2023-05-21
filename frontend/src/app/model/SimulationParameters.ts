export class SimulationParameters {
    /**
     * This class represents the simulation parameters to be sent to the server.
     * 
     * @param iterations - the number of iterations to be performed
     * @samplingFrequency - the sampling frequency of the simulation in Hz
     * @param stringFrequency - the fundamental frequency of the string in Hz
     * @param stringTension - the tension of the string in N
     * @param soundboardReflectionCoefficient - the reflection coefficient of the soundboard
     * @param hammerMass - the mass of the hammer in g
     * @param linearFeltStiffness - the linear stiffness of the felt in N/m
     * @param hammerRelativeStrikingPoint - the relative striking point of the hammer in % 
     * @param hammerInitialVelocity - the initial velocity of the hammer in m/s
     * @param hammerStringDistance - the distance between the hammer and the string in cm
     */
    private iterations: number = 88200;
    private samplingFrequency: number = 44100;
    private stringFrequency: number = 440;
    private stringTension: number = 670;
    private soundboardReflectionCoefficient:number = 0.98;
    private hammerMass: number = 8.71;
    private linearFeltStiffness = 1000;
    private hammerRelativeStrikingPoint: number = 0.116;
    private hamerInitialVelocity: number = 7;
    private hammerStringDistance: number = 0.01;

    constructor(iterations: number, 
        samplingFrequency: number, 
        stringFrequency: number, 
        stringTension: number, 
        soundboardReflectionCoefficient: number,
        hammerMass: number,
        linearFeltStiffness: number,
        hammerRelativeStrikingPoint: number,
        hammerInitialVelocity: number,
        hammerStringDistance: number) {
            this.iterations = iterations;
            this.samplingFrequency = samplingFrequency; 
            this.stringFrequency = stringFrequency;     
            this.stringTension = stringTension; 
            this.soundboardReflectionCoefficient = soundboardReflectionCoefficient; 
            this.hammerMass = hammerMass;
            this.linearFeltStiffness = linearFeltStiffness;   
            this.hammerRelativeStrikingPoint = hammerRelativeStrikingPoint; 
            this.hamerInitialVelocity = hammerInitialVelocity;  
            this.hammerStringDistance = hammerStringDistance;   
    }

    public getIterations(): number {
        return this.iterations;
    }

    public getSamplingFrequency(): number {
        return this.samplingFrequency;
    }

    public getStringFrequency(): number {
        return this.stringFrequency
    }

    public getStringTension(): number {
        return this.stringTension
    }

    public getSoundboardReflectionCoefficient(): number {   
        return this.soundboardReflectionCoefficient;
    }       

    public getHammerMass(): number {
        return this.hammerMass;
    }   

    public getLinearFeltStiffness(): number {
        return this.linearFeltStiffness;
    }

    public getHammerRelativeStrikingPoint(): number {
        return this.hammerRelativeStrikingPoint;
    }

    public getHammerInitialVelocity(): number {
        return this.hamerInitialVelocity;
    }

    public getHammerStringDistance(): number {
        return this.hammerStringDistance;
    }
}