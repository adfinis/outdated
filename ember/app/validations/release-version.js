import { validatePresence } from 'ember-changeset-validations/validators';

import validateDate from '../validators/other-date';
export default {
  endOfLifeDate: [
    validatePresence({ presence: true, ignoreBlank: true }),
    validateDate({ after: 'releaseDate' }),
  ],
};
