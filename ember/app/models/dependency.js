import Model, { attr } from '@ember-data/model';

export default class DependencyModel extends Model {
  @attr name;
  @attr provider;

  get url() {
    const providerMap = {
      PIP: 'https://pypi.org/project/',
      NPM: 'https://npmjs.com/package/',
    };

    return providerMap[this.provider] + this.name;
  }
}
