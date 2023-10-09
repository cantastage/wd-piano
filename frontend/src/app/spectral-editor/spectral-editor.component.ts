import { Component, Input } from '@angular/core';
import { DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS, SpectralAnalysisParameters, SpectralFeatures } from '../model/daap-features';
import { ApiService } from '../api.service';
import { API_URL } from 'src/env';

@Component({
  selector: 'app-spectral-editor',
  templateUrl: './spectral-editor.component.html',
  styleUrls: ['./spectral-editor.component.scss']
})
export class SpectralEditorComponent {
  @Input() filenames: Array<string> = []; // results in compare mode
  spectralParameters: SpectralAnalysisParameters = DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS;
  spectralFeatures: SpectralFeatures;
  baseFilename: string;
  isUpdating = false;
  windowLengthOptions: Array<number> = [64, 128, 256, 512, 1024, 2048, 4096, 8192];
  hopLengthOptions: Array<number> = [64, 128, 256, 512, 1024, 2048, 4096, 8192];
  fftLengthOptions: Array<number> = [256, 512, 1024, 2048, 4096, 8192];
  selectedWinLength: number = 0;
  showPlots: boolean = true;
  errorMsg: string = '';
  showErrorMsg: boolean = false;
  plotVersionIndex: number = 0; // used to force update of plots

  constructor(private apiService: ApiService) {
    this.spectralFeatures = {
      mfccs: '',
      spectralCentroid: '',
      spectralBandwidth: '',
      spectralContrast: '',
      spectralRollOff: '',
      tonnetz: ''
    };
    this.baseFilename = 'wd-compare' + Date.now().toString();
  }

  public updateComparisonPlots(): void {
    this.isUpdating = true; // disable button
    if (this.checkSpectralParams()) {
      // call to serviceAPI
      this.apiService.updateComparisonPlots(this.baseFilename, this.filenames, this.spectralParameters, this.plotVersionIndex)
      .subscribe((data: any) => {
        this.spectralFeatures = data.daapFeatures;
        console.log('Arrived comparison plots names from server:');
        console.log(data.daapFeatures);
        this.isUpdating = false;
      });
      this.plotVersionIndex++; // increase plot version index
    } else {
      this.isUpdating = false;
    }
  }

  public getPlotUrl(plotName: string): string {
    return API_URL + '/plot/' + plotName;
  }
  
  private checkSpectralParams(): boolean {
    if (this.spectralParameters.winLength > this.spectralParameters.nFFT) {
      this.errorMsg = 'NOTE: Window length cannot be greater than FFT length';
      this.showErrorMsg = true;
      return false;
    } else {
      this.showErrorMsg = false;
      return true;
    }
  }


}
