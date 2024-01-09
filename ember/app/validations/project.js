import {
  validatePresence,
  validateLength,
  validateFormat,
  validateInclusion,
} from 'ember-changeset-validations/validators';

import validationsWhenOther from 'outdated/utils/validations-when-other';

export default {
  name: [
    validatePresence({ presence: true, ignoreBlank: true }),
    validateLength({ max: 100 }),
  ],
  repoType: [validatePresence(true)],
  repo: [
    validatePresence({ presence: true, ignoreBlank: true }),
    validateLength({ max: 200 }),
    validateFormat({
      regex: /^([-_\w]+\.[-._\w]+)\/([-_\w]+)\/([-_\w]+)$/,
    }),
  ],
  accessToken: validationsWhenOther({
    field: 'repoType',
    otherFieldValidator: validateInclusion({ in: ['access-token'] }),
    fieldValidators: [
      validatePresence({ presence: true, ignoreBlank: true }),
      validateFormat({ regex: /^[-_a-zA-Z\d]*$/ }),
    ],
  }),
  maintainers: [],
};
