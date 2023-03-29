import Model, { attr, hasMany } from '@ember-data/model';

export default class ProjectModel extends Model {
  @attr name;
  @attr status;
  @attr('django-url') repo;
  @hasMany('dependency-version') dependencyVersions;
}
