import Model, { attr, belongsTo } from '@ember-data/model';

export default class VersionModel extends Model {
  @attr patchVersion;
  @attr('django-date') releaseDate;
  @belongsTo('releaseVersion') releaseVersion;
}
