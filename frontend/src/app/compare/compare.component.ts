import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { LocalDataService } from '../local-data.service';
import { DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS, SpectralAnalysisParameters } from '../model/daap-features';
import { WDResult } from '../model/wd-result';

@Component({
  selector: 'app-compare',
  templateUrl: './compare.component.html',
  styleUrls: ['./compare.component.scss']
})
export class CompareComponent {
  wdResults: Array<WDResult>;
  spectralParameters: SpectralAnalysisParameters;

  constructor(private apiService: ApiService, private dataService: LocalDataService) { 
    this.wdResults = this.dataService.getSavedWDResults();
    this.spectralParameters = DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS;
  }
}
