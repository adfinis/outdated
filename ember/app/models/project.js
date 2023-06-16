import Model, { attr, hasMany } from '@ember-data/model';
import { tracked } from '@glimmer/tracking';

export default class ProjectModel extends Model {
  @attr name;
  @attr status;
  @attr repo;
  @hasMany('version') versionedDependencies;
  @hasMany('maintainer') maintainers;

  @tracked users;
  @tracked primaryMaintainer;
}
