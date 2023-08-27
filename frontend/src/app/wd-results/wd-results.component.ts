import { Component, Input } from '@angular/core';
import { WDResult } from '../model/wd-result';

@Component({
  selector: 'app-wd-results',
  templateUrl: './wd-results.component.html',
  styleUrls: ['./wd-results.component.scss']
})
export class WdResultsComponent {
  @Input() results: Array<WDResult> = [];

  constructor() { }

}
