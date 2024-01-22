import Model, { attr, belongsTo } from '@ember-data/model';

export default class VersionModel extends Model {
  @attr patchVersion;
  @attr('django-date') releaseDate;
  @belongsTo('releaseVersion', { inverse: null, async: false }) releaseVersion;

  get name() {
    return this.releaseVersion.get('dependency.name');
  }
  get endOfLife() {
    return this.releaseVersion.get('endOfLife');
  }

  get version() {
    return `${this.releaseVersion.get('releaseVersion')}.${this.patchVersion}`;
  }
  get requirements() {
    return `${this.name} ${this.version}`;
  }
  get status() {
    return this.releaseVersion.get('status');
  }
  get url() {
    const providerMap = {
      PIP: `https://pypi.org/project/${this.name}/`,
      NPM: `https://npmjs.org/package/${this.name}/v/`,
    };

    return providerMap[this.releaseVersion.dependency.provider] + this.version;
  }
}
