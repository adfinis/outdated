import Model, { attr, hasMany } from '@ember-data/model';
import { tracked } from '@glimmer/tracking';

export default class ProjectModel extends Model {
  @attr name;
  @attr status;
  @attr({ defaultValue: 'https' }) repoProtocol;
  @attr repo;
  @hasMany('version', { inverse: null, async: false }) versionedDependencies;
  @hasMany('maintainer', { inverse: 'project', async: false }) maintainers;

  @tracked users;
  @tracked primaryMaintainer;

  get repoURL() {
    return `${this.repoProtocol}://${this.repo}`;
  }
}
