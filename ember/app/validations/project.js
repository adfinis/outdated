import {
  validatePresence,
  validateLength,
  validateFormat,
} from 'ember-changeset-validations/validators';

export default {
  name: [validatePresence(true), validateLength({ max: 100 })],
  repo: [
    validatePresence(true),
    validateLength({ max: 200 }),
    validateFormat({ type: 'url' }),

    validateFormat({
      regex: /^(\s)*https?:\/\//,
      message: '{description} must start with either http:// or https://',
    }),
  ],
  maintainers: [],
};
