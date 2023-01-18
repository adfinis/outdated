import { Factory, trait } from 'miragejs';
import { faker } from '@faker-js/faker';

export default Factory.extend({
  name: () =>
    faker.helpers.arrayElement([
      faker.random.word() +
        faker.helpers.arrayElement(['y ', 'x ', 'io ']) +
        faker.helpers.arrayElement([
          'webapp',
          'application',
          'frontend',
          'backend',
        ]),
      'ember ' +
        faker.helpers.arrayElement([
          'uikit',
          faker.word.adjective() + ' helpers',
          'caluma',
        ]),
      faker.name.jobArea() + 'y',
      faker.helpers.arrayElement(['ember', 'caluma', 'python', 'django']) +
        ' ' +
        faker.word.verb(),
    ]),
  repo() {
    return (
      'https://github.com/' +
      faker.internet.domainWord() +
      '/' +
      faker.helpers.slugify(this.name)
    );
  },
  status: () =>
    faker.helpers.arrayElement(['OUTDATED', 'WARNING', 'UP-TO-DATE']),

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
