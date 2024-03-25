import Model, { attr, hasMany, belongsTo } from '@ember-data/model';
import { tracked } from 'tracked-built-ins';

export default class DependencySourceModel extends Model {
  @attr status;
  @attr path;

  @hasMany('version', { inverse: null, async: false }) versions;
  @hasMany('maintainer', { inverse: 'source', async: false, as: 'source' })
  maintainers;
  @belongsTo('project', {
    inverse: 'sources',
    async: true,
    as: 'dependency-source',
  })
  project;

  @tracked users;
  @tracked primaryMaintainer;
}
