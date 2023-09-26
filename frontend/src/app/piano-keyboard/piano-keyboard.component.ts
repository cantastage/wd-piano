import { Component, Output, EventEmitter } from '@angular/core';
import { ApiService } from '../api.service';
import { PianoKey } from '../model/piano-key';
import { style } from '@angular/animations';

@Component({
  selector: 'app-piano-keyboard',
  templateUrl: './piano-keyboard.component.html',
  styleUrls: ['./piano-keyboard.component.scss']
})
export class PianoKeyboardComponent {
  // private pianoToMidiOffset = 20; // 20 is the offset from piano key to corresponding midi note number
  // private numKeys = 88; // 88 keys on a piano
  // unwrappedStringKeys: Array<PianoKey> = []; // TODO maybe add getter and make field private
  keyLabels: Array<string> = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  currentOctaveIndex: number = 4; // octave index of the keyboard
  @Output() selectedKeyEvent = new EventEmitter<string>(); // selected key in the piano keyboard

  // ngOnInit() {
  //   this.apiService.getStrings().subscribe((data) => {
  //     // console.log("ARRIVED FROM SERVER: ", data);
  //     this.unwrappedStringKeys = this.parsePianoKeys(data);
  //   });
  // }

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


  /**
   * Selects class for keyboard key based on the note label
   * @param pianoKeyIndex 
   * @returns 
   */
  public getPianoKeyStyle(pianoKeyIndex: number): string {
    let noteLabel = this.keyLabels[pianoKeyIndex];
    // TODO check if it can be optimized
    let styleClass = "";
    // console.log("root note label for index " + pianoKeyIndex + ": ", noteLabel);
    if (noteLabel.includes("#",1)) {
      styleClass = "black " + noteLabel[0].toLowerCase() + "s"; 
    } else {
      styleClass = "white " + noteLabel[0].toLowerCase();
    }
    // console.log("piano-key styleClass: ", styleClass);
    return styleClass;
  }

  public getNoteLabelStyle(pianoKeyIndex: number): string {
    let noteLabel = this.keyLabels[pianoKeyIndex];
    return noteLabel.includes("#",1) ? "black-note-label" : "white-note-label";
  }

  /**
   * Selects a key and emits an event for the parent component to set the simulation parameters of the corresponding key
   * @param pianoKeyIndex 
   */
  public selectPianoKey(pianoKeyIndex: number): void {
    let formattedKeyLabel = this.keyLabels[pianoKeyIndex] + this.currentOctaveIndex;
    console.log("selected key: ", formattedKeyLabel);
    this.selectedKeyEvent.emit(formattedKeyLabel);
  }

  public changeOctave(octaveAdder: number): void {
    if ((octaveAdder == -1 && this.currentOctaveIndex > 1) || (octaveAdder == 1 && this.currentOctaveIndex < 7)) {
      this.currentOctaveIndex += octaveAdder;
    }
  }
}