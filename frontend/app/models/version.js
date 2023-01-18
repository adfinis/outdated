import Model, { attr, belongsTo, hasMany } from '@ember-data/model';

export default class VersionModel extends Model {
  @attr version;
  @attr status;
  @attr('date') eolDate;
  @attr('date') releaseDate;
  @belongsTo('dependency') dependency;
  @hasMany('project') projects;
}
