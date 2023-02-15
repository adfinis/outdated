import { faker } from '@faker-js/faker';
import { DateTime } from 'luxon';
import { Factory, trait } from 'miragejs';

export default Factory.extend({
  version: () => faker.system.semver(),
  eolDate: () => faker.date.future(2),
  releaseDate: () => faker.date.past(4),

  status() {
    const eolDateTime = DateTime.fromJSDate(this.eolDate);
    const now = DateTime.now();
    if (eolDateTime < now) {
      return 'OUTDATED';
    } else if (eolDateTime < now.plus({ months: 1 })) {
      return 'WARNING';
    }
    return 'UP-TO-DATE';
  },

  isEndOfLife: trait({
    eolDate: () => faker.date.recent(),
  }),
  isNearlyEndOfLife: trait({
    eolDate: () => faker.date.soon(25),
  }),

  afterCreate(version, server) {
    server.create('dependency', { versions: [version] });
  },
});
