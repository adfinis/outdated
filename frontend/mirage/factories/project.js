import { Factory, trait } from 'miragejs';
import { faker } from '@faker-js/faker';

export default Factory.extend({
  name: () => faker.commerce.productName(),
  repo: () => faker.internet.url(),

  withVersions: trait({
    afterCreate(project, server) {
      server.createList('version', 10, { projects: [project] });
      server.createList('version', 3, 'isEndOfLife', { projects: [project] });
    },
  }),
});
