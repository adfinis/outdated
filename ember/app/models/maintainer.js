import Model, { attr, belongsTo } from '@ember-data/model';

export default class ReleaseVersionModel extends Model {
  @attr isPrimary;
  @belongsTo('project') project;
  @belongsTo('user') user;
}
