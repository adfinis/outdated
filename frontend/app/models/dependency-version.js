import Model, { attr, belongsTo, hasMany } from '@ember-data/model';

export default class DependencyVersionModel extends Model {
  @attr version;
  @attr status;
  @attr('django-date') endOfLifeDate;
  @attr('django-date') releaseDate;
  @belongsTo('dependency') dependency;
  @hasMany('project') projects;
}
