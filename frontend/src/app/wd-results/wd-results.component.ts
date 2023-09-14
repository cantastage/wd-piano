import { ChangeDetectorRef, Component, Input, SimpleChanges } from '@angular/core';
import { WDResult } from '../model/wd-result';
import { API_URL } from 'src/env';
import { DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS, EMPTY_SPECTRAL_FEATURES, SpectralAnalysisParameters, SpectralFeatures } from '../model/daap-features';
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
  selectedWinLength: number = 0;
  showPlots: boolean = true;
  errorMsg: string = '';
  showErrorMsg: boolean = false;

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

  private checkSpectralParams(resultIndex: number): boolean {
    if (this.spectralParameters[resultIndex].winLength > this.spectralParameters[resultIndex].nFFT) {
      this.errorMsg = 'NOTE: Window length cannot be greater than FFT length';
      this.showErrorMsg = true;
      return false;
    } else {
      return true;
    }
  }


  public getFFTSelectOptions(index: number, spectralParam: string): Array<number> {
    switch (spectralParam) {
      case 'winLength':
        return this.fftLengthOptions.filter((value) => value <= this.spectralParameters[index].nFFT);
    }
    return this.fftLengthOptions;
  }

  // TODO maybe add error management
  /**
   * Update spectral features plots
   * @param resultIndex index of the result to update
   */
  public updatePlots(resultIndex: number): void {
    this.isUpdating = true; // disable button
    if (this.checkSpectralParams(resultIndex)) {
      // this.togglePlots(resultIndex);
      // this.showPlots = false;
      // call to serviceAPI
      let baseFilename = this.results[resultIndex].baseFilename;
      // this.spectralParameters[resultIndex].baseFilename = this.results[resultIndex].baseFilename;
      this.apiService.updatePlots(baseFilename, this.spectralParameters[resultIndex])
        .subscribe((data: any) => {
          // console.log('Arrived updated plots names from server:');
          // console.log(data);
          this.results[resultIndex].daapFeatures = EMPTY_SPECTRAL_FEATURES;
          this.results[resultIndex].daapFeatures = data.daapFeatures;
          console.log('Arrived updated plots names from server:');
          console.log(data.daapFeatures);
          // this.triggerFetchPlots(resultIndex);
          this.isUpdating = false;
          // this.togglePlots(resultIndex);
        });
    } else {
      this.isUpdating = false;
    }
  }

  // private triggerFetchPlots(resultIndex: number): void {
  //   let mfccUrlBackup = this.results[resultIndex].daapFeatures.mfccs;
  //   this.results[resultIndex].daapFeatures.mfccs = '';
  //   this.results[resultIndex].daapFeatures.mfccs = mfccUrlBackup;

  // }
  public togglePlots(index: number) {
    this.showPlots = !this.showPlots;
  }

  public getPlotUrl(plotName: string): string {
    return API_URL + '/plot/' + plotName;
  }

  public getVideoUrl(videoIndex: number): string {
    let videoName = this.results[videoIndex].videoFilename;
    return API_URL + '/video/' + videoName;
  }
}
