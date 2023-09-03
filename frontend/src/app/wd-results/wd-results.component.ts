import { Component, Input, SimpleChanges } from '@angular/core';
import { WDResult } from '../model/wd-result';
import { API_URL } from 'src/env';

@Component({
  selector: 'app-wd-results',
  templateUrl: './wd-results.component.html',
  styleUrls: ['./wd-results.component.scss']
})
export class WdResultsComponent {
  @Input() results: Array<WDResult> = [];

  constructor() {
    // this.results.push(new WDResult('C4-Default', [], {mfccs: 'mfccs-C4-default', spectralCentroid: 'spectralCentroid-C4-default'}));
   }

  // ngOnChanges(changes: SimpleChanges) {
  //   console.log("Arrived new results: ", changes);
  //   this.results = changes['results'].currentValue;
  // }

  public getPlotUrl(plotName: string): string {
    return API_URL + '/plot/' + plotName;
  }

  public getVideoUrl(videoIndex: number): string {
    let videoName = this.results[videoIndex].videoFilename;
    return API_URL + '/video/' + videoName;
  }
}
