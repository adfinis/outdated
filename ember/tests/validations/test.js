import {
  validatePresence,
  validateLength,
} from 'ember-changeset-validations/validators';

export default {
  test: [validatePresence(true), validateLength({ min: 4 })],
};
