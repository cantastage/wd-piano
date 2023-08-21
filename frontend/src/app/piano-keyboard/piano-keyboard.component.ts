import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { PianoKey } from '../model/piano-strings';

@Component({
  selector: 'app-piano-keyboard',
  templateUrl: './piano-keyboard.component.html',
  styleUrls: ['./piano-keyboard.component.scss']
})
export class PianoKeyboardComponent {
  // private pianoToMidiOffset = 20; // 20 is the offset from piano key to corresponding midi note number
  // private numKeys = 88; // 88 keys on a piano
  private unwrappedStrings: Array<PianoKey> = [];

  ngOnInit() {
    this.apiService.getStrings().subscribe((data) => {
      // console.log("ARRIVED FROM SERVER: ", data);
      this.unwrappedStrings = this.parsePianoKeys(data);
    });
  }

  constructor(private apiService: ApiService) {
  }

  // /**
  //  * Calculates the center frequency of the piano keyboard note
  //  * @param pianoKeyIndex 
  //  * @returns 
  //  */
  // public getKeyCenterFrequency(pianoKeyIndex: number): number {
  //   let centerFreq = 440 * Math.pow(2, (pianoKeyIndex - 49) / 12);
  //   return centerFreq;
  // }

  // /**
  //  * Calculates the name of the piano keyboard MIDI note
  //  * @param pianoKeyIndex 
  //  * @returns 
  //  */
  // public getMidiNoteLabel(pianoKeyIndex: number): string {

  //   let midiNote = pianoKeyIndex + this.pianoToMidiOffset;
  //   return midiNote.toString();
  // }

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