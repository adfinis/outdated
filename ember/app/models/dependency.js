import Model, { attr } from '@ember-data/model';

export default class DependencyModel extends Model {
  @attr name;
  @attr status;
}
