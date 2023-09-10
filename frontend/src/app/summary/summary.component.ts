import { Component, Input } from '@angular/core';
import { WDParam } from '../model/wd-settings';

@Component({
  selector: 'app-summary',
  templateUrl: './summary.component.html',
  styleUrls: ['./summary.component.scss']
})
export class SummaryComponent {
  @Input() params: Array<WDParam> = [];
  
}
