import { get } from '@ember/object';

export default function validateWhenOther(options = {}) {
  return (key, value, oldValue, changes, content) => {
    const { field, otherFieldValidator, fieldValidator } = options;
    const fieldValue = get(changes, field) || get(content, field);

    const result = otherFieldValidator(field, fieldValue, null, null, null);
    if (result !== true) return true;

    return fieldValidator(key, value, oldValue, changes, content);
  };
}
