import { validatePresence } from 'ember-changeset-validations/validators';

export default {
  version: [validatePresence(true)],
};
