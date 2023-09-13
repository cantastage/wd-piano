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
  @Input() spectralParameters: Array<SpectralAnalysisParameters> = [];
  // spectralParameters: SpectralAnalysisParameters;
  isUpdating = false;
  fftLengthOptions: Array<number> = [64, 128, 256, 512, 1024, 2048, 4096, 8192];

  constructor(private apiService: ApiService) {
    // this.spectralParameters = DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS;
    // this.spectralParameters.push(DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS);
  }

  // ngOnChanges(changes: SimpleChanges) {
  //   console.log('ENTRA IN ONCHANGES');
  //   if (changes['current'] != changes['previous']) {
  //     console.log('changes detected in wd-results.component.ts: ', changes);
  //   }
  // }


  // public getFFTSelectOptions(spectralParam: string): Array<number> {
  //  switch (spectralParam) {
  //   case 'winLength':
  //     return this.fftLengthOptions.filter((value) => value <= this.spectralParameters[].nFFT);
  //  } 
  //  return this.fftLengthOptions;
  // }


  public updatePlots(resultIndex: number): void {
    this.isUpdating = true;
    // call to serviceAPI
    this.spectralParameters[resultIndex].baseFilename = this.results[resultIndex].baseFilename;
    this.apiService.updatePlots(this.spectralParameters[resultIndex]);
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
