import Model, { attr, hasMany } from '@ember-data/model';

export default class ProjectModel extends Model {
  @attr name;
  @attr status;
  @attr repo;
  @attr({ defaultValue: 'public' }) repoType;
  @attr accessToken;

  @hasMany('dependency-source', {
    inverse: 'project',
    async: false,
    as: 'project',
    polymorphic: true,
  })
  sources;

  get repoURL() {
    return `https://${this.repo}`;
  }
}
