import { Factory, trait } from 'miragejs';
import { faker } from '@faker-js/faker';
export default Factory.extend({
  version: () => faker.system.semver(),
  eolDate: () => faker.date.soon(),
  relaseDate: () => faker.date.past(),

  isEndOfLife: trait({
    eolDate: () => faker.date.recent(),
  }),
  afterCreate(version, server) {
    server.create('dependency', { versions: [version] });
  },
});
