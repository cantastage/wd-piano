import { Component, Output } from '@angular/core';
import { ApiService } from '../api.service';
import { SimpleWDParam, WDParam, WDPARAMS } from '../model/wd-settings';
import { API_URL } from 'src/env';
import { PianoKey } from '../model/piano-key';
import { WDResult } from '../model/wd-result';

@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.scss']
})
export class EditorComponent {

  // UI flags to show parameters panel
  showPianoKeyboard: boolean = true;
  showProMode: boolean = true;
  isRendered: boolean = true; //true if the simulation video has been rendered
  setWgLengthMode = 0; // 0 = set f0, 1 = set length and sound speed

  // Parameters related fields
  wdParams: WDParam[]; //contains all the parameters for the simulation
  pianoKeys: Array<PianoKey> = []; // TODO maybe add getter and make field private
  paramsContainer: Map<string, SimpleWDParam>;

  wdResults: Array<WDResult> = [];

  ngOnInit() {
    this.apiService.getPianoKeys().subscribe((data) => {
      // console.log("ARRIVED FROM SERVER: ", data);
      this.pianoKeys = this.parsePianoKeys(data);
    });
  }

  constructor(private apiService: ApiService) {
    this.wdResults.push(new WDResult('C4-Default.mp4', [], { 
      mfccs: 'mfccs-C4-default.png', 
      spectralCentroid: 'spectralCentroid-C4-default.png', 
      spectralBandwidth: 'spectralBandwidth-C4-default.png', 
      spectralContrast: 'spectralContrast-C4-default.png',
      spectralRollOff: 'spectralRollOff-C4-default.png', 
      tonnetz:'tonnetz-C4-default.png'
    }));
    this.wdParams = WDPARAMS; // retrieves from model the default parameters for the simulation
    this.paramsContainer = new Map<string, WDParam>();
    this.initWDParams();
  }

  // TODO complete method with error management
  public runWDPiano(): void {
    this.isRendered = false;
    this.apiService.runWDPiano(this.parseWDParams())
      .subscribe((data: WDResult) => {
        console.log('Arrived from server:');
        console.log(data);
        this.wdResults.push(data);
        this.isRendered = true;
      });
  }

  selectFs(value: string) {
    this.wdParams[1].value = parseInt(value);
    console.log('Selected Fs: ', this.wdParams[1].value);
  }

  toggleSetWGLengthMode(modeIndex: number) {
    this.setWgLengthMode = modeIndex;
  }

  /**
   * Sets the parameters related to a particular piano key
   * @param keyLabel name label of the piano key
   */
  setWDPianoKeyParams(keyLabel: string): void {
    let translatedLabel = keyLabel;
    if (keyLabel.includes("#", 1)) {
      translatedLabel = keyLabel.replace("#", "d");
    }
    console.log('key label: ', keyLabel);
    let selectedKey: PianoKey | undefined = this.pianoKeys.find(key => key.getNoteLabel() == translatedLabel);
    if (selectedKey !== undefined) {
      this.wdParams[3].value = selectedKey.getCenterFrequency();
      this.wdParams[4].value = (selectedKey.getStringLength()); // we need to display it in cm
      this.wdParams[5].value = selectedKey.getStringDiameter();
      this.wdParams[6].value = selectedKey.getStringTension();
      this.wdParams[8].value = selectedKey.getHammerMass();
      this.wdParams[9].value = parseFloat((selectedKey.getHammerImpactPosition() / selectedKey.getStringLength() * 100).toFixed(2)); // we need to display it in %
      console.log('calculated relative striking point: ', this.wdParams[9].value);
    }
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
    this.wdParams[0].value = this.wdParams[0].value * this.wdParams[1].value; // iterations = (duration in seconds) * samplingFrequency
    let jsonParams: Object[] = Object.assign(this.wdParams.map(key => ({ [key.name]: key.value })));
    let finalObj = {};
    jsonParams.forEach(obj => { Object.assign(finalObj, obj) });
    console.log('Parsed wdParams to send to server:');
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
