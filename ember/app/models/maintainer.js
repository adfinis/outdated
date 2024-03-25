import Model, { attr, belongsTo } from '@ember-data/model';

export default class MaintainerModel extends Model {
  @attr isPrimary;
  @belongsTo('source', {
    inverse: 'maintainers',
    async: true,
    as: 'maintainer',
    polymorphic: true,
  })
  source;
  @belongsTo('user', { inverse: null, async: false }) user;
}
