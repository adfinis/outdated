import { faker } from '@faker-js/faker';
import { Factory, trait } from 'miragejs';

export default Factory.extend({
  name: () => `${faker.hacker.adjective()} ${faker.company.bsNoun()}`,
  status: () => 'UNDEFINED',
  repoType: () => faker.helpers.arrayElement(['public', 'access-token']),

  repo() {
    return `github.com/${faker.internet.domainWord()}/${faker.helpers.slugify(
      this.name,
    )}`;
  },
  withMaintainers: trait({
    afterCreate(project, server) {
      project.update({
        sources: [
          server.create('dependency-source', 'withMaintainers', { project }),
        ],
      });
    },
  }),
  withSources: trait({
    status: () =>
      faker.helpers.arrayElement(['OUTDATED', 'WARNING', 'UP-TO-DATE']),

    afterCreate(project, server) {
      project.update({
        sources: [
          server.create('dependency-source', 'withVersions', { project }),
          server.create('dependency-source', { project }),
        ],
      });
    },
  }),
});
