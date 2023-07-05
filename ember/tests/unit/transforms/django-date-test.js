import { module, test } from 'qunit';

import { setupTest } from 'outdated/tests/helpers';

module('Unit | Transform | django date', function (hooks) {
  setupTest(hooks);

  test('serializes', function (assert) {
    const transform = this.owner.lookup('transform:django-date');
    const testDate = '1991-02-20';
    const result = transform.serialize(new Date(testDate));
    assert.strictEqual(result, testDate);
  });

  test('deserializes', function (assert) {
    const transform = this.owner.lookup('transform:django-date');

    assert.notOk(transform.deserialize(''));
    assert.notOk(transform.deserialize(null));

    const testDate = '1991-02-20';
    const result = transform.deserialize(testDate);
    assert.strictEqual(result.toString(), new Date(testDate).toString());
  });
});
