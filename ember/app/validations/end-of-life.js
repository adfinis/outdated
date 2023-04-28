import {
  validatePresence,
  validateDate,
} from 'ember-changeset-validations/validators';

export default {
  endOfLife: [validatePresence(true), validateDate()],
};
