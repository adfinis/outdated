import { Factory, hasMany } from 'miragejs';
import { faker } from '@faker-js/faker';
export default Factory.extend({
  name: () =>
    faker.helpers.arrayElement([
      'ember-',
      'caluma-',
      'django-',
      'py-',
      'postgres-',
      'embroider-',
      'ember-cli-',
      '@ember/',
      'eslint-plugin-',
    ]) +
    faker.helpers.arrayElement([
      faker.hacker.ingverb(),
      faker.word.adjective(),
      faker.company.bsAdjective(),
      faker.hacker.verb(),
      faker.company.bsBuzz(),
      faker.system.commonFileExt() +
        faker.helpers.arrayElement(['-support', '-export', '-import']),
    ]),
  versions: hasMany(),
});
