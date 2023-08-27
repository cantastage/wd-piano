import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PianoKeyboardComponent } from './piano-keyboard/piano-keyboard.component';
import { EditorComponent } from './editor/editor.component';
import {MatSliderModule} from '@angular/material/slider';
import {MatCardModule} from '@angular/material/card';
import { FormsModule } from '@angular/forms';
import { CamelcaseToWordsPipe } from './camelcase-to-words.pipe';
import { VideoPlayerComponent } from './video-player/video-player.component';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { ParametersComponent } from './parameters/parameters.component';
import { HsDataDirective } from './hs-data.directive';
import { WdResultsComponent } from './wd-results/wd-results.component';
@NgModule({
  declarations: [
    AppComponent,
    PianoKeyboardComponent,
    EditorComponent,
    CamelcaseToWordsPipe,
    VideoPlayerComponent,
    ParametersComponent,
    HsDataDirective,
    WdResultsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatSliderModule,
    MatCardModule,
    FormsModule,
    ScrollingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
