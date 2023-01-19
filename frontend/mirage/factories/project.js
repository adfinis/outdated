import { Factory, trait } from 'miragejs';
import { faker } from '@faker-js/faker';

export default Factory.extend({
  name: () => faker.hacker.adjective() + ' ' + faker.company.bsNoun(),

  status: () =>
    faker.helpers.arrayElement(['OUTDATED', 'WARNING', 'UP-TO-DATE']),

  repo() {
    return (
      'https://github.com/' +
      faker.internet.domainWord() +
      '/' +
      faker.helpers.slugify(this.name)
    );
  },
  withVersions: trait({
    afterCreate(project, server) {
      server.createList('version', 3, 'isEndOfLife', { projects: [project] });

      server.createList('version', 3, 'isNearlyEndOfLife', {
        projects: [project],
      });

      server.createList('version', 10, { projects: [project] });
    },
  }),
});
