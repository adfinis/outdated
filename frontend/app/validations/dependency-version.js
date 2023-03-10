import {
  validatePresence,
  validateLength,
  validateFormat,
  validateDate,
} from 'ember-changeset-validations/validators';

export default {
  version: [
    validatePresence(true),
    validateLength({ max: 100 }),
    validateFormat({
      regex:
        /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/,
    }),
  ],
  eolDate: [
    validatePresence(true),
    validateDate({ after: new Date('1991-02-20') }),
  ],
  releaseDate: [
    validatePresence(true),
    validateDate({
      before: new Date(),
      after: new Date('1991-02-20'),
    }),
  ],
};
