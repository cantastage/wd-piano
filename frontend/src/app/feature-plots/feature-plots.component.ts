import { Component, Input, SimpleChange } from '@angular/core';
import { API_URL } from 'src/env';
import { SpectralFeatures } from '../model/daap-features';

@Component({
  selector: 'app-feature-plots',
  templateUrl: './feature-plots.component.html',
  styleUrls: ['./feature-plots.component.scss']
})
export class FeaturePlotsComponent {
  @Input() daapFeatures: SpectralFeatures = {mfccs:'', spectralCentroid:'', spectralBandwidth:'', spectralContrast:'', spectralRollOff:'', tonnetz:''};

  // ngOnInit() {
  //   console.log('feature-plots urls: ', this.daapFeatures);
  // }

  public getPlotUrl(plotName: string): string {
    // let time = new Date().getTime();
    return API_URL + '/plot/' + plotName;
  }
}
