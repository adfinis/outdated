import Model, { attr, belongsTo } from '@ember-data/model';

export default class VersionModel extends Model {
  @attr patchVersion;
  @attr('django-date') releaseDate;
  @belongsTo('releaseVersion') releaseVersion;

  get name() {
    return this.releaseVersion.get('dependency').get('name');
  }
  get endOfLife() {
    return this.releaseVersion.get('endOfLife');
  }

  get version() {
    const releaseVersion = this.releaseVersion;
    return `${releaseVersion.get('releaseVersion')}.${this.patchVersion}`;
  }
  get requirements() {
    return `${this.name} ${this.version}`;
  }
  get status() {
    return this.releaseVersion.get('status');
  }
}
