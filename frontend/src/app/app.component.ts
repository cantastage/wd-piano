import { Component } from '@angular/core';
import { API_URL } from 'src/env';
import { ApiService } from './api.service';
// import { saveAs } from 'file-saver';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  appTitle: string = 'WDF-Piano';
  videoURL: string = API_URL + '/static/videos/Visualizer.mp4';
  video: File;
  constructor(private apiService: ApiService) {
    this.video = new File([], 'sto');
  }

  ngOnInit() {
    // this.apiService.downloadVideo().subscribe(blob => this.fileSaver.save(blob, 'wdf-piano-example.mp4'));
  }
}
