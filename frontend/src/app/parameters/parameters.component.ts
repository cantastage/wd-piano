import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { WDParam, WDPARAMS } from '../model/wd-settings';

@Component({
  selector: 'app-parameters',
  templateUrl: './parameters.component.html',
  styleUrls: ['./parameters.component.scss']
})
export class ParametersComponent {

  private wdParams: WDParam[]; //contains all the parameters for the simulation

  constructor(private apiService: ApiService) {
    this.wdParams = WDPARAMS;
  }

  // TODO complete method with return result
  runSimulation(): void {
    this.apiService.runSimulation(this.getWDParams())
      .subscribe((data) => {
        console.log('Returned data: ' + data)
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
