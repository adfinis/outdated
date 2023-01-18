import Model, { attr, hasMany } from '@ember-data/model';

export default class ProjectModel extends Model {
  @attr name;
  @attr status;
  @attr repo;
  @hasMany('version') versions;
}
