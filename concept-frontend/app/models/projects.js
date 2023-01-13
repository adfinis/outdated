import Model, { attr } from '@ember-data/model';

export default class ProjectsModel extends Model {
  @attr name;
  @attr repo;
}
