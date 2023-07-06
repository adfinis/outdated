import { module, test } from 'qunit';

import TestValidations from 'outdated/tests/validations/test';
import emptyChangeset from 'outdated/utils/empty-changeset';

module('Unit | Utility | EmptyChangeset', function () {
  test('it works', function (assert) {
    const result = emptyChangeset(TestValidations);
    assert.ok(result);
  });
});
