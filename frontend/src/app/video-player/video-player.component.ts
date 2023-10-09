import { Component, Input } from '@angular/core';
import { API_URL } from 'src/env';

@Component({
  selector: 'app-video-player',
  templateUrl: './video-player.component.html',
  styleUrls: ['./video-player.component.scss']
})
export class VideoPlayerComponent {
 @Input() videoUrl: string = ''; //url of the video to be rendered
}
