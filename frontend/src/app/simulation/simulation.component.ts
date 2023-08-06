import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { WDParam, WDPARAMS } from '../model/wd-settings';

@Component({
  selector: 'app-simulation',
  templateUrl: './simulation.component.html',
  styleUrls: ['./simulation.component.scss']
})
export class SimulationComponent {

  wdParams: WDParam[]; //contains all the parameters for the simulation

  isRendered: boolean = false; //true if the simulation has been rendered
  videoUrl: string = ''; //url of the video to be rendered

  constructor(private apiService: ApiService) {
    this.wdParams = WDPARAMS;
  }

  // TODO complete method with return result
  runSimulation(): void {
    this.isRendered = false;
    this.apiService.runSimulation(this.getWDParams())
      .subscribe((data) => {
        // console.log(data.videoUrl);
        this.videoUrl = data.videoUrl;
        console.log('extracted videoUrl: ' + this.videoUrl)
        this.isRendered = true;
      });
  }

  private getWDParams(): Object {
    let jsonParams: Object[] = Object.assign(this.wdParams.map(key => ({ [key.name]: key.value })));
    let finalObj = {};
    jsonParams.forEach(obj => {Object.assign(finalObj, obj)});
    console.log(finalObj);
    return finalObj;
  }
}
