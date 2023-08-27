import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WdResultsComponent } from './wd-results.component';

describe('WdResultsComponent', () => {
  let component: WdResultsComponent;
  let fixture: ComponentFixture<WdResultsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WdResultsComponent]
    });
    fixture = TestBed.createComponent(WdResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
