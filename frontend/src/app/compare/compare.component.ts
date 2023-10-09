import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { LocalDataService } from '../local-data.service';
import { DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS, SpectralAnalysisParameters } from '../model/daap-features';
import { WDResult } from '../model/wd-result';
import { API_URL } from 'src/env';

@Component({
  selector: 'app-compare',
  templateUrl: './compare.component.html',
  styleUrls: ['./compare.component.scss']
})
export class CompareComponent {
  wdResults: Array<WDResult>;
  spectralParameters: SpectralAnalysisParameters;

  ngOnInit() {
    this.wdResults = this.wdResults.filter(wdResult => wdResult.compare); // selects only results that are checked for comparison
  }

  constructor(private apiService: ApiService, private dataService: LocalDataService) { 
    this.wdResults = this.dataService.getSavedWDResults();
    this.spectralParameters = DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS;
  }

  public getCompareFilenames(): Array<string> {
    return this.wdResults.map(wdResult => wdResult.baseFilename);
  }

  public getPlotUrl(plotName: string): string {
    return API_URL + '/plot/' + plotName;
  }


}
