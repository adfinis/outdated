import validateOtherDate from 'outdated/validators/other-date';
import { module, test } from 'qunit';

module('Unit | Validator | other-date');
test('it works with after', function (assert) {
  assert.true(
    validateOtherDate({ after: 'otherKey' })(
      'key',
      new Date(2000, 1, 1),
      null,
      {},
      { otherKey: new Date(1990, 1, 1) }
    )
  );
  assert.strictEqual(
    typeof validateOtherDate({ after: 'otherKey' })(
      'key',
      new Date(1990, 1, 1),
      null,
      {},
      { otherKey: new Date(2000, 1, 1) }
    ),
    'string'
  );
});

test('it works with before', function (assert) {
  assert.true(
    validateOtherDate({ before: 'otherKey' })(
      'key',
      new Date(1990, 1, 1),
      null,
      {},
      { otherKey: new Date(2000, 1, 1) }
    )
  );
  assert.strictEqual(
    typeof validateOtherDate({ before: 'otherKey' })(
      'key',
      new Date(2000, 1, 1),
      null,
      {},
      { otherKey: new Date(1990, 1, 1) }
    ),
    'string'
  );
});
