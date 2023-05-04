import { faker } from '@faker-js/faker';
import { DateTime } from 'luxon';
import { Factory, trait } from 'miragejs';

export default Factory.extend({
  majorVersion: () => faker.datatype.number({ min: 1, max: 10 }),
  minorVersion: () => faker.datatype.number({ min: 0, max: 10 }),
  endOfLife: () => faker.date.future(2),

  status() {
    const eolDateTime = DateTime.fromJSDate(this.endOfLife);
    const now = DateTime.now();
    if (eolDateTime < now) {
      return 'OUTDATED';
    } else if (eolDateTime < now.plus({ months: 1 })) {
      return 'WARNING';
    }
    return 'UP-TO-DATE';
  },

  isEndOfLife: trait({
    endOfLifeDate: () => faker.date.recent(),
  }),
  isNearlyEndOfLife: trait({
    endOfLifeDate: () => faker.date.soon(80),
  }),

  afterCreate(releaseVersion, server) {
    releaseVersion.update({ dependency: server.create('dependency') });
  },
});
