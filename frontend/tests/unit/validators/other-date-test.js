import validateOtherDate from 'outdated/validators/other-date';
import { module, test } from 'qunit';

module('Unit | Validator | other-date');

test('it exists', function (assert) {
  assert.ok(validateOtherDate());
});
