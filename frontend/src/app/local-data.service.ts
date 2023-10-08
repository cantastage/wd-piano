import { Injectable } from '@angular/core';
import { WDResult } from './model/wd-result';
import { SpectralAnalysisParameters } from './model/daap-features';

@Injectable({
  providedIn: 'root'
})
export class LocalDataService {
  private wdResults: Array<WDResult>;
  private spectralParameters: Array<SpectralAnalysisParameters>;
  constructor() { 
    this.wdResults = [];
    this.spectralParameters = [];
  }

  // "Getters"
  public getSavedWDResults(): Array<WDResult> {
    return this.wdResults;
  }

  public getSavedSpectralParameters(): Array<SpectralAnalysisParameters> {
    return this.spectralParameters;
  }

  // Setters

  public saveWDResults(wdResults: Array<WDResult>) {
    this.wdResults = wdResults;
  }


  public saveSpectralParameters(spectralParameters: Array<SpectralAnalysisParameters>) {
    this.spectralParameters = spectralParameters;
  }
} 
