import Model, { attr, belongsTo, hasMany } from '@ember-data/model';

export default class DependencyVersionModel extends Model {
  @attr version;
  @attr status;
  @attr('date') endOfLifeDate;
  @attr('date') releaseDate;
  @belongsTo('dependency') dependency;
  @hasMany('project') projects;
}
