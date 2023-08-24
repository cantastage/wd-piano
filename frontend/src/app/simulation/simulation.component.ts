import { Component, Output } from '@angular/core';
import { ApiService } from '../api.service';
import { SimpleWDParam, WDParam, WDPARAMS } from '../model/wd-settings';
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
  pianoKeys: Array<PianoKey> = []; // TODO maybe add getter and make field private
  paramsContainer: Map<string, SimpleWDParam>;

  videoUrl: string = ''; //url of the video to be rendered
  // @Output() selectedKey: string = "C4";  //key selected by the user

  ngOnInit() {
    this.apiService.getPianoKeys().subscribe((data) => {
      // console.log("ARRIVED FROM SERVER: ", data);
      this.pianoKeys = this.parsePianoKeys(data);
    });  
  }

  constructor(private apiService: ApiService) {
    this.wdParams = WDPARAMS; // retrieves from model the default parameters for the simulation
    this.paramsContainer = new Map<string, WDParam>();
    this.initWDParams();
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
   * Sets the parameters related to a particular piano key
   * @param keyLabel name label of the piano key
   */
  setWDPianoKeyParams(keyLabel: string): void {
    let translatedLabel = keyLabel;
    if(keyLabel.includes("#",1)) {
      translatedLabel = keyLabel.replace("#", "d");
    }
    console.log('key label: ', keyLabel);
    let selectedKey: PianoKey | undefined = this.pianoKeys.find(key => key.getNoteLabel() == translatedLabel);
    if (selectedKey !== undefined) {
      // set parameters
      // for (let i=0; i<this.wdParams.length; i++) { 
      //   this.
      // }
      // this.wdParams.find(param => param.name == 'stringFundamentalFrequency').value = 262.22;
      this.wdParams[3].value = selectedKey.getCenterFrequency();
      this.wdParams[4].value = selectedKey.getStringLength()*100; // we need to display it in cm
      this.wdParams[5].value = selectedKey.getStringDiameter();
      this.wdParams[6].value = selectedKey.getStringTension();
      this.wdParams[8].value = selectedKey.getHammerMass();
      this.wdParams[9].value = selectedKey.getHammerImpactPosition()/selectedKey.getStringLength()*100; // we need to display it in %
      console.log('calculated relative striking point: ', this.wdParams[9].value);
      // this.wdParams[12].value = selectedKey.getHammerElasticityCoefficient();
    }
    // if ()
    // this.wdParams.find(param => param.name == 'stringFundamentalFrequency').value = selectedKey.getCenterFrequency();
    // this.wdParams.find(param => param.name == 'stringLength').value = selectedKey.getStringLength();
    // this.wdParams.find(param => param.name == 'stringDiameter').value = selectedKey.getStringDiameter();
    // this.wdParams.find(param => param.name == 'stringTension').value = selectedKey.getStringTension();
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

  // TODO change according to new model of simulation parameters
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

  private initWDParams(): void {
    // this.paramsContainer = new Map<string, WDParam>(); // già nel costruttore
    for (let i = 0; i < this.wdParams.length; i++) {
      this.paramsContainer.set(this.wdParams[i].name, this.wdParams[i]);
    }
  }
}
