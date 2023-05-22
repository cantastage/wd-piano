import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PianoKeyboardComponent } from './piano-keyboard/piano-keyboard.component';
import { ParametersComponent } from './parameters/parameters.component';
import {MatSliderModule} from '@angular/material/slider';
import {MatCardModule} from '@angular/material/card';
import { FormsModule } from '@angular/forms';
import { CamelcaseToWordsPipe } from './camelcase-to-words.pipe';

@NgModule({
  declarations: [
    AppComponent,
    PianoKeyboardComponent,
    ParametersComponent,
    CamelcaseToWordsPipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatSliderModule,
    MatCardModule,
    FormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
