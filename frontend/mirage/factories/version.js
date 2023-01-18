import { Factory, trait } from 'miragejs';
import { faker } from '@faker-js/faker';
import { DateTime } from 'luxon';

export default Factory.extend({
  version: () => faker.system.semver(),
  eolDate: () => faker.date.future(2),
  releaseDate: () => faker.date.past(4),



  status() {
    let eolDateTime = DateTime.fromJSDate(this.eolDate)
    if (eolDateTime < DateTime.now()) {
      return 'OUTDATED';
    } else if (eolDateTime < DateTime.now().plus({months: 1})) {
      return 'WARNING';
    }
    return 'UP-TO-DATE';
  },

    isEndOfLife: trait({
    eolDate: () => faker.date.recent(),
  }),
  isNearlyEndOfLife: trait({
    eolDate : () => faker.date.soon(25),
  }),

  afterCreate(version, server) {
    server.create('dependency', { versions: [version] });
  },
});
