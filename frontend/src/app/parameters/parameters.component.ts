import { Component } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-parameters',
  templateUrl: './parameters.component.html',
  styleUrls: ['./parameters.component.scss']
})
export class ParametersComponent {
  constructor(private apiService:ApiService) { }
}
