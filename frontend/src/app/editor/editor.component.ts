import { Component, Output } from '@angular/core';
import { ApiService } from '../api.service';
import { SimpleWDParam, WDParam, WDPARAMS } from '../model/wd-settings';
import { API_URL } from 'src/env';
import { PianoKey } from '../model/piano-key';
import { WDResult } from '../model/wd-result';
import { DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS, SpectralAnalysisParameters } from '../model/daap-features';

@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.scss']
})
export class EditorComponent {
  // UI related fields
  isRendered: boolean = true; //true if the simulation video has been rendered
  currentWgLengthMode: number = 0; // 0 = set f0, 1 = set length and sound speed
  // Parameters related fields
  wdParams: WDParam[]; //contains all the parameters for the simulation
  pianoKeys: Array<PianoKey> = []; // contains all the piano keys data
  wdResults: Array<WDResult> = []; // contains all runs of the algorithm
  spectralParameters: Array<SpectralAnalysisParameters> = [];

  ngOnInit() {
    this.apiService.getPianoKeys().subscribe((data) => {
      // console.log("ARRIVED FROM SERVER: ", data);
      this.pianoKeys = this.parsePianoKeys(data);
    });
  }

  constructor(private apiService: ApiService) {
    this.spectralParameters.push(DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS);
    this.wdParams = WDPARAMS; // retrieves from model the default parameters for the simulation
    this.wdResults.push(new WDResult(
      'C4-Default',
      'C4-Default.mp4',
      this.wdParams, {
      mfccs: 'mfccs-C4-default.png',
      spectralCentroid: 'spectralCentroid-C4-default.png',
      spectralBandwidth: 'spectralBandwidth-C4-default.png',
      spectralContrast: 'spectralContrast-C4-default.png',
      spectralRollOff: 'spectralRollOff-C4-default.png',
      tonnetz: 'tonnetz-C4-default.png'
    }));
  }

  // TODO complete method with error management
  /**
   * Run WD-Piano algorithm
   */
  public runWDPiano(): void {
    this.isRendered = false;
    let summary = this.wdParams;
    let parsedParams = this.parseWDParams();
    this.apiService.runWDPiano(parsedParams, DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS)
      .subscribe((data: WDResult) => {
        console.log('Arrived from server:');
        console.log(data);
        data.paramSummary = summary;
        this.wdResults.push(data);
        this.spectralParameters.push(DEFAULT_SPECTRAL_ANALYSIS_PARAMETERS);
        this.isRendered = true;
      });
  }

  /**
   * Binds fs to model and parses int value
   * @param value 
   */
  public selectFs(value: string): void {
    this.wdParams[1].value = parseInt(value);
    console.log('Selected Fs: ', this.wdParams[1].value);
  }

  /**
   * Toggles the way wgLength is calculated
   * @param wgLengthMode wgLength calculation mode
   */
  public toggleSetWGLengthMode(wgLengthMode: number): void {
    this.currentWgLengthMode = wgLengthMode;
  }

  /**
   * Sets the parameters related to a particular piano key
   * @param keyLabel name label of the piano key
   */
  public setWDPianoKeyParams(keyLabel: string): void {
    let translatedLabel = keyLabel;
    if (keyLabel.includes("#", 1)) {
      translatedLabel = keyLabel.replace("#", "d");
    }
    // console.log('key label: ', keyLabel);
    let selectedKey: PianoKey | undefined = this.pianoKeys.find(key => key.getNoteLabel() == translatedLabel);
    if (selectedKey !== undefined) {
      this.wdParams[3].value = selectedKey.getCenterFrequency();
      this.wdParams[4].value = (selectedKey.getStringLength()); // we need to display it in cm
      this.wdParams[5].value = selectedKey.getStringDiameter();
      this.wdParams[6].value = selectedKey.getStringTension();
      this.wdParams[8].value = selectedKey.getHammerMass();
      // this.wdParams[9].value = parseFloat((selectedKey.getHammerImpactPosition() / selectedKey.getStringLength() * 100).toFixed(2)); // we need to display it in %
      let hammerImpactPosition = selectedKey.getHammerImpactPosition();
      let stringLength = selectedKey.getStringLength();
      this.wdParams[9].value = parseFloat(((hammerImpactPosition / stringLength) * 100).toFixed(2)); // // we need to display it in %
      console.log('calculated relative striking point: ', this.wdParams[9].value);
    }
  }

  public updateWgLengthParams(wgLengthMode: number): void {
    if (wgLengthMode === 0) {
      this.wdParams[4].value = (this.wdParams[2].value / (2 * this.wdParams[3].value)); // L = c/(2*f0) [cm]
    } else {
      this.wdParams[3].value = 100 * (this.wdParams[2].value / (2 * this.wdParams[4].value)); // f0 = c/(2*L) [Hz]
    }
  }

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
        parseFloat(splitted[2]), // stringLength in cm,
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
