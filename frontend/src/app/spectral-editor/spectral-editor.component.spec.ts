import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpectralEditorComponent } from './spectral-editor.component';

describe('SpectralEditorComponent', () => {
  let component: SpectralEditorComponent;
  let fixture: ComponentFixture<SpectralEditorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SpectralEditorComponent]
    });
    fixture = TestBed.createComponent(SpectralEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
