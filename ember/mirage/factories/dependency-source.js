import { faker } from '@faker-js/faker';
import { Factory, trait } from 'miragejs';

export default Factory.extend({
  path: () =>
    [
      faker.helpers.arrayElement([
        'app',
        'web',
        'api',
        'frontend',
        'backend',
        'ember',
      ]),
      faker.helpers.arrayElement([
        'poetry.lock',
        'pnpm-lock.yaml',
        'yarn.lock',
      ]),
    ].join('/'),
  status: () => 'UNDEFINED',

  withVersions: trait({
    status: () =>
      faker.helpers.arrayElement(['OUTDATED', 'WARNING', 'UP-TO-DATE']),

    afterCreate(source, server) {
      source.update({
        versions: [
          server.create('version', 'isEndOfLife'),
          server.create('version', 'isNearlyEndOfLife'),
          server.create('version'),
        ],
      });
    },
  }),

  withMaintainers: trait({
    afterCreate(source, server) {
      source.update({
        maintainers: [
          server.create('maintainer', {
            user: server.create('user'),
            source,
            isPrimary: true,
          }),
          server.create('maintainer', {
            user: server.create('user'),
            source,
          }),
        ],
      });
    },
  }),
});
