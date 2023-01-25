import Model, { attr, hasMany } from '@ember-data/model';

export default class DependencyModel extends Model {
  @attr name;
  @hasMany('dependency-version') versions;
}
