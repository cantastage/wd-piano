import { Component } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-parameters',
  templateUrl: './parameters.component.html',
  styleUrls: ['./parameters.component.scss']
})
export class ParametersComponent {
  minStringFrequency: number = 0;
  maxStringFrequency: number = 20000;
  stringFrequency = 440;
  minStringTension: number = 0; // TODO check suitable range
  maxStringTension: number = 1000; // TODO check suitable range
  stringTension: number = 670;
  minHammerMass: number = 0; // TODO check suitable range
  maxHammerMass: number = 1000; // TODO check suitable range
  hammerMass: number = 0;
  minHammerInitialVelocity: number = 0; // TODO check suitable range
  maxHammerInitialVelocity: number = 1000; // TODO check suitable range
  hammerInitialVelocity: number = 0;
  minHammerStrikePoint: number = 0; // TODO check suitable range
  maxHammerStrikePoint: number = 1000; // TODO check suitable range
  hammerStrikePoint: number = 0;


  value = 0;

  // DEBUG only TODO remove after testing
  formatLabel(value: number): string {
    if (value >= 1000) {
      return Math.round(value / 1000) + 'k';
    }

    return `${value}`;
  }
  constructor(private apiService:ApiService) { }
}
