import Model, { attr, belongsTo } from '@ember-data/model';

export default class MaintainerModel extends Model {
  @attr isPrimary;
  @belongsTo('project', { inverse: 'maintainers', async: true }) project;
  @belongsTo('user', { inverse: null, async: false }) user;
}
