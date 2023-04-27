import { faker } from '@faker-js/faker';
import { Factory, trait } from 'miragejs';

export default Factory.extend({
  patchVersion: () => faker.datatype.number({ min: 1, max: 10 }),
  releaseDate: () => faker.date.past(2),

  afterCreate(version, server) {
    version.update({ releaseVersion: server.create('release-version') });
  },

  isEndOfLife: trait({
    afterCreate(version, server) {
      version.update({
        releaseVersion: server.create('release-version', 'isEndOfLife'),
      });
    },
  }),
  isNearlyEndOfLife: trait({
    afterCreate(version, server) {
      version.update({
        releaseVersion: server.create('release-version', 'isNearlyEndOfLife'),
      });
    },
  }),
});
