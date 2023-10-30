import { Factory, belongsTo } from 'miragejs';

export default Factory.extend({
  project: belongsTo(),
  user: belongsTo(),
  isPrimary: (index) => index === 0,
});
