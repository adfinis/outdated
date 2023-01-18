import { module, test } from 'qunit';
import { setupTest } from 'outdated/tests/helpers';

module('Unit | Route | project-detailed', function (hooks) {
  setupTest(hooks);

  test('it exists', function (assert) {
    let route = this.owner.lookup('route:project-detailed');
    assert.ok(route);
  });
});
