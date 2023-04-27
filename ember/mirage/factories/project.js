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
      project.update({
        versionedDependencies: [
          server.create('version', 'isEndOfLife'),
          server.create('version', 'isNearlyEndOfLife'),
          server.create('version'),
        ],
      });
    },
  }),
});
