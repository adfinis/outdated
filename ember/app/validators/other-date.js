import { get } from '@ember/object';
import getMessages from 'ember-changeset-validations/utils/get-messages';
import buildMessage from 'ember-changeset-validations/utils/validation-errors';

export default function validateDate(options = {}) {
  return (key, value, oldValue, changes, content) => {
    const { after, before } = options;
    if (after) {
      const afterVal = get(changes, after) || get(content, after);
      if (value <= afterVal) {
        return buildMessage(key, {
          type: 'after',
          value,
          context: { after: getMessages().getDescriptionFor(after) },
        });
      }
    }
    if (before) {
      const beforeVal = get(changes, before) || get(content, before);
      if (value >= beforeVal) {
        return buildMessage(key, {
          type: 'before',
          value,
          context: { before: getMessages().getDescriptionFor(before) },
        });
      }
    }
    return true;
  };
}
