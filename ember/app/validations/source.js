import { validatePresence } from 'ember-changeset-validations/validators';

export default {
  users: [validatePresence(true)],
  primaryMaintainer: [],
};
