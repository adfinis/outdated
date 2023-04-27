import Model, { attr, belongsTo } from '@ember-data/model';

export default class ReleaseVersionModel extends Model {
  @attr majorVersion;
  @attr minorVersion;
  @attr status;
  @attr latestPatchVersion;
  @attr('django-date') endOfLife;
  @belongsTo('dependency') dependency;
}
