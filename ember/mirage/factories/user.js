import { faker } from '@faker-js/faker';
import { Factory } from 'miragejs';

export default Factory.extend({
  idpId: () => faker.string.uuid,
  firstName: () => faker.person.firstName(),
  lastName: () => faker.person.lastName(),
  email: () => faker.internet.email(),
  username: () => faker.internet.userName(),
});
