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
  keyLabels: Array<string> = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  currentOctaveIndex: number = 4; // octave index of the keyboard
  @Output() selectedKeyEvent = new EventEmitter<string>(); // selected key in the piano keyboard

  constructor(private apiService: ApiService) {
  }

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