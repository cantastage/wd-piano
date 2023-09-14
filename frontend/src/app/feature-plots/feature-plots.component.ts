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

  ngOnChanges(changes: SimpleChange) {
    // this.daapFeatures = changes['daapFeatures'].currentValue;
  }

  ngOnInit() {
    console.log('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
    console.log('feature-plots urls: ', this.daapFeatures);
  }

  public getPlotUrl(plotName: string): string {
    return API_URL + '/plot/' + plotName;
  }
}
