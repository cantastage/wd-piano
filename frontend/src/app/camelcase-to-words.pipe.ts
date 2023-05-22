import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'camelcaseToWords'
})
export class CamelcaseToWordsPipe implements PipeTransform {

  transform(phrase: string): string {
    return phrase.replace(/^[a-z]/g, char => ` ${char.toUpperCase()}`)
    .replace(/[A-Z]|[0-9]+/g, ' $&')
    .replace(/(?:\s+)/, char => '');
  }
}
