import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FeaturePlotsComponent } from './feature-plots.component';

describe('FeaturePlotsComponent', () => {
  let component: FeaturePlotsComponent;
  let fixture: ComponentFixture<FeaturePlotsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FeaturePlotsComponent]
    });
    fixture = TestBed.createComponent(FeaturePlotsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
