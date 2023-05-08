import { Component } from '@angular/core';
import { API_URL } from 'src/env';
import { ApiService } from './api.service';
// import { saveAs } from 'file-saver';
import { FileSaverService } from 'ngx-filesaver';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  videoURL: string = API_URL + '/static/videos/Visualizer.mp4';
  video: File;
  constructor(private apiService: ApiService, private fileSaver: FileSaverService) {
    this.video = new File([], 'sto');
  }

  ngOnInit() {
    // this.apiService.downloadVideo().subscribe(blob => this.fileSaver.save(blob, 'wdf-piano-example.mp4'));
  }

  runSimulation(): void {
    this.apiService.runSimulation().subscribe(() => console.log('Simulation started'));
  }
}
