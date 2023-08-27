import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[hsData]'
})
export class HsDataDirective {

  constructor(public viewContainerRef: ViewContainerRef) { }

}
