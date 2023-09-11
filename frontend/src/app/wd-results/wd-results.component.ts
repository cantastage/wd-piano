import { Component, Input, SimpleChanges } from '@angular/core';
import { WDResult } from '../model/wd-result';
import { API_URL } from 'src/env';
import { DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS, SpectralAnalysisParameters } from '../model/daap-features';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-wd-results',
  templateUrl: './wd-results.component.html',
  styleUrls: ['./wd-results.component.scss']
})
export class WdResultsComponent {
  @Input() results: Array<WDResult> = [];
  spectralParameters: SpectralAnalysisParameters;
  isUpdating = false;

  constructor(private apiService: ApiService) {
    this.spectralParameters = DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS;
  }


  public updatePlots(resultIndex: number): void {
    this.isUpdating = true;
    // call to serviceAPI
    this.spectralParameters.baseFilename = this.results[resultIndex].videoFilename;
    this.apiService.updatePlots(this.spectralParameters);
    this.isUpdating = false;
  }


  public getPlotUrl(plotName: string): string {
    return API_URL + '/plot/' + plotName;
  }

  public getVideoUrl(videoIndex: number): string {
    let videoName = this.results[videoIndex].videoFilename;
    return API_URL + '/video/' + videoName;
  }
}
