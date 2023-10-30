import { faker } from '@faker-js/faker';
import { Factory } from 'miragejs';

export default Factory.extend({
  idpId: () => faker.string.uuid,
  firstName: () => faker.person.firstName(),
  lastName: () => faker.person.lastName(),
  email() {
    return `${this.firstName}.${this.lastName}@example.com`.toLowerCase();
  },
  username() {
    return `${this.firstName}${this.lastName[0]}`.toLowerCase();
  },
});
