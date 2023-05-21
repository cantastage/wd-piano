import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { SimulationParameters } from '../model/SimulationParameters';

@Component({
  selector: 'app-parameters',
  templateUrl: './parameters.component.html',
  styleUrls: ['./parameters.component.scss']
})
export class ParametersComponent {
  // NOTE: all default values are referred to the C4 note of the piano
  iterations: number = 88200;
  minIterations: number = 1;
  maxIterations: number = 200000;
  samplingFrequency: number = 44100; // in Hz
  stringFrequency = 262.22; // in Hz
  minStringFrequency: number = 20; // in Hz
  maxStringFrequency: number = 20000; // in Hz
  stringTension: number = 670; // in N
  minStringTension: number = 400; // in N
  maxStringTension: number = 1000; // in N
  stringLength: number = 65.7; // in cm
  minStringLength: number = 5; // in cm
  maxStringLength: number = 500; // in cm 
  stringDiameter: number = 1.064; // in mm
  minStringDiameter: number = 0.5; // in mm
  maxStringDiameter: number = 2; // in mm
  soundBoardReflectionCoefficient: number = 0.98;
  minSoundboardReflectionCoefficient: number = 0; // TODO check suitable range
  maxSoundboardReflectionCoefficient: number = 1; // TODO check suitable range
  hammerMass: number = 8.71;
  minHammerMass: number = 5; 
  maxHammerMass: number = 10; 
  linearFeltStiffness: number = 1000;
  minLinearFeltStiffness: number = 0; // TODO check suitable range
  maxLinearFeltStiffness: number = 10000; // TODO check suitable range
  hammerInitialVelocity: number = 7;
  minHammerInitialVelocity: number = 0; // TODO check suitable range
  maxHammerInitialVelocity: number = 10; // TODO check suitable range
  hammerRelativeStrikingPoint: number = 0.116;
  minHammerRelativeStrikingPoint: number = 0; 
  maxHammerRelativeStrikingPoint: number = 1; 
  hammerStringDistance: number = 10; // cm
  minHammerStringDistance: number = 0; // cm
  maxHammerStringDistance: number = 30; // cm

  value = 0;

  // DEBUG only TODO remove after testing
  formatLabel(value: number): string {
    if (value >= 1000) {
      return Math.round(value / 1000) + 'k';
    }

    return `${value}`;
  }
  constructor(private apiService:ApiService) { }

  // TODO complete method with return result
  runSimulation(): void {
    this.apiService.runSimulation(this.packSimulationParameters())
    .subscribe((data) => {
      console.log('Returned data: ' + data)
    });
  }

  private packSimulationParameters(): SimulationParameters {
    let simulationSettings = new SimulationParameters(this.iterations,
      this.samplingFrequency,
      this.stringFrequency,
      this.stringTension,
      this.stringLength,
      this.stringDiameter,
      this.soundBoardReflectionCoefficient,
      this.hammerMass,
      this.linearFeltStiffness,
      this.hammerRelativeStrikingPoint,
      this.hammerInitialVelocity,
      this.hammerStringDistance);
      return simulationSettings;
  }
}
