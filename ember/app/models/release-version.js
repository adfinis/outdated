import Model, { attr, belongsTo } from '@ember-data/model';

export default class ReleaseVersionModel extends Model {
  @attr majorVersion;
  @attr minorVersion;
  @attr status;

  @attr('django-date') endOfLife;
  @belongsTo('dependency', { inverse: null, async: false }) dependency;

  get releaseVersion() {
    return `${this.majorVersion}.${this.minorVersion}`;
  }
  get name() {
    return `${this.dependency.get('name')} ${this.releaseVersion}`;
  }
}
