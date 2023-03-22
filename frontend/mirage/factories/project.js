import { faker } from '@faker-js/faker';
import { Factory, trait } from 'miragejs';

export default Factory.extend({
  name: () => `${faker.hacker.adjective()} ${faker.company.bsNoun()}`,
  status: () => 'UNDEFINED',

  repo() {
    return `https://github.com/${faker.internet.domainWord()}/${faker.helpers.slugify(
      this.name
    )}`;
  },
  withVersions: trait({
    status: () =>
      faker.helpers.arrayElement(['OUTDATED', 'WARNING', 'UP-TO-DATE']),

    afterCreate(project, server) {
      server.createList('dependency-version', 1, 'isEndOfLife', {
        projects: [project],
      });

      server.createList('dependency-version', 2, 'isNearlyEndOfLife', {
        projects: [project],
      });

      server.createList('dependency-version', 3, { projects: [project] });
    },
  }),
});
