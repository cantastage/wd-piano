import { CamelcaseToWordsPipe } from './camelcase-to-words.pipe';

describe('CamelcaseToWordsPipe', () => {
  it('create an instance', () => {
    const pipe = new CamelcaseToWordsPipe();
    expect(pipe).toBeTruthy();
  });
});
