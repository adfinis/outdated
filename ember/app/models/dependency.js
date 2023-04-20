import Model, { attr, hasMany } from '@ember-data/model';

export default class DependencyModel extends Model {
  @attr name;
  @attr latest;
  @hasMany('dependency-version') versions;
}
