import { faker } from '@faker-js/faker';
import { DateTime } from 'luxon';
import { Factory, trait } from 'miragejs';

export default Factory.extend({
  majorVersion: () => faker.datatype.number({ min: 1, max: 10 }),
  minorVersion: () => faker.datatype.number({ min: 0, max: 10 }),
  endOfLife: () => faker.date.future(20),

  status() {
    const dayDiff = DateTime.fromJSDate(this.endOfLife)
      .diff(DateTime.now(), 'days')
      .toObject().days;
    if (dayDiff <= 0) {
      return 'OUTDATED';
    } else if (dayDiff <= 150) {
      return 'WARNING';
    }
    return 'UP-TO-DATE';
  },

  isEndOfLife: trait({
    endOfLife: () => faker.date.recent(),
  }),
  isNearlyEndOfLife: trait({
    endOfLife: () => faker.date.soon(80),
  }),

  afterCreate(releaseVersion, server) {
    releaseVersion.update({ dependency: server.create('dependency') });
  },
});
