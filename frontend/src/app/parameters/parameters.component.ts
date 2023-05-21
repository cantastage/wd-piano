import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { SimulationParameters } from '../model/SimulationParameters';

@Component({
  selector: 'app-parameters',
  templateUrl: './parameters.component.html',
  styleUrls: ['./parameters.component.scss']
})
export class ParametersComponent {
  iterations: number = 88200;
  minIterations: number = 1;
  maxIterations: number = 200000;
  samplingFrequency: number = 44100;
  stringFrequency = 262.22; // C4
  minStringFrequency: number = 0;
  maxStringFrequency: number = 20000;
  stringTension: number = 670;
  minStringTension: number = 0; // TODO check suitable range
  maxStringTension: number = 1000; // TODO check suitable range
  soundBoardReflectionCoefficient: number = 0.98;
  minSoundboardReflectionCoefficient: number = 0; // TODO check suitable range
  maxSoundboardReflectionCoefficient: number = 1; // TODO check suitable range
  hammerMass: number = 0;
  minHammerMass: number = 0; // TODO check suitable range
  maxHammerMass: number = 1000; // TODO check suitable range
  linearFeltStiffness: number = 1000;
  minLinearFeltStiffness: number = 0; // TODO check suitable range
  maxLinearFeltStiffness: number = 10000; // TODO check suitable range
  hammerInitialVelocity: number = 0;
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
  runSimulation(simulationParams: SimulationParameters): void {
    this.apiService.runSimulation(simulationParams)
    .subscribe((data) => {
      console.log('Returned data: ' + data)
    });
  }
}
