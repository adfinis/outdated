import { validatePresence } from 'ember-changeset-validations/validators';

export default {
  dependency: [validatePresence(true)],
};
