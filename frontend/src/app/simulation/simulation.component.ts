import { Component, Output } from '@angular/core';
import { ApiService } from '../api.service';
import { WDParam, WDPARAMS } from '../model/wd-settings';
import { API_URL } from 'src/env';
import { PianoKey } from '../model/piano-strings';

@Component({
  selector: 'app-simulation',
  templateUrl: './simulation.component.html',
  styleUrls: ['./simulation.component.scss']
})
export class SimulationComponent {

  // UI flags to show parameters panel
  showPianoKeyboard: boolean = true;
  showProMode: boolean = true;
  isRendered: boolean = false; //true if the simulation video has been rendered

  // Parameters related fields
  wdParams: WDParam[]; //contains all the parameters for the simulation
  unwrappedStringKeys: Array<PianoKey> = []; // TODO maybe add getter and make field private


  videoUrl: string = ''; //url of the video to be rendered
  @Output() selectedKey: string = "C4";  //key selected by the user

  ngOnInit() {
    this.apiService.getStrings().subscribe((data) => {
      // console.log("ARRIVED FROM SERVER: ", data);
      this.unwrappedStringKeys = this.parsePianoKeys(data);
    });
  }

  constructor(private apiService: ApiService) {
    this.wdParams = WDPARAMS; // retrieves from model the default parameters for the simulation
  }

  // TODO complete method with error management
  runSimulation(): void {
    this.isRendered = false;
    this.apiService.runSimulation(this.parseWDParams())
      .subscribe((data) => {
        console.log('returned video name from server: ' + data.videoFilename);
        this.videoUrl = API_URL + '/video/' + data.videoFilename;
        console.log('extracted videoUrl: ' + this.videoUrl)
        this.isRendered = true;
      });
  }

  
  /** 
   * Toggles piano keyboard view
   */
  public togglePianoView() {
    this.showPianoKeyboard = !this.showPianoKeyboard;
  }

  /**
   * Toggles expert mode parameters editing view
   */
  public toggleProMode() {
    this.showProMode = !this.showProMode;
  }


  private parseWDParams(): Object {
    let jsonParams: Object[] = Object.assign(this.wdParams.map(key => ({ [key.name]: key.value })));
    let finalObj = {};
    jsonParams.forEach(obj => { Object.assign(finalObj, obj) });
    console.log(finalObj);
    return finalObj;
  }

  private parsePianoKeys(rawKeys: Array<string>): Array<PianoKey> {
    let pianoKeys: Array<PianoKey> = []; // init array of piano key objects
    for (let i = 0; i < rawKeys.length; i++) {
      let rawKey: String = rawKeys[i][0];
      let splitted = rawKey.split(";", 18); // split the values of the key
      // console.log('Split rawKey: ', splitted);
      let pianoKey = new PianoKey(
        splitted[0], // noteLabel
        parseFloat(splitted[1]), // centerFrequency,
        parseFloat(splitted[2]), // stringLength,
        parseFloat(splitted[3]), // stringDiameter,
        parseFloat(splitted[4]), // stringVolumetricDensity,
        parseInt(splitted[5]), // stringTension,
        parseFloat(splitted[12]), // hammerNonLinearElasticExponent,
        parseFloat(splitted[13]), // hammerImpactPosition,
        parseFloat(splitted[14]), // hammerMass,
        parseFloat(splitted[15]), // hammerElasticityCoefficient
      );
      pianoKeys.push(pianoKey);
    }
    return pianoKeys;
  }
}
