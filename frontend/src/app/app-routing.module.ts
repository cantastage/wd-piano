import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EditorComponent } from './editor/editor.component';
import { HeroComponent } from './hero/hero.component';
import { CompareComponent } from './compare/compare.component';

const routes: Routes = [
  { path: 'editor', component: EditorComponent },
  { path: 'home', component: HeroComponent },
  { path: 'compare', component: CompareComponent },
  { path: '', redirectTo: 'home', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
