import {
  validatePresence,
  validateLength,
  validateFormat,
  validateDate,
} from 'ember-changeset-validations/validators';
import validateOtherDate from 'outdated/validators/other-date';

export default {
  version: [
    validatePresence({ presence: true, ignoreBlank: true }),
    validateLength({ max: 100 }),
    validateFormat({
      regex:
        /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/,
      message: '{description} should be a valid semantic version',
    }),
    validateOtherDate({ after: 'releaseDate' }),
  ],
  endOfLifeDate: [
    validatePresence({ presence: true, ignoreBlank: true }),
    validateDate({ after: new Date('1991-02-20') }),
  ],
  releaseDate: [
    validatePresence({ presence: true, ignoreBlank: true }),
    validateDate({
      before: new Date(),
      after: new Date('1991-02-20'),
      message: '{description} must be a valid date',
    }),
    validateOtherDate({ before: 'endOfLifeDate' }),
  ],
};
