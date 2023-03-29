import { setupTest } from 'outdated/tests/helpers';
import { module, test } from 'qunit';

module('Unit | Transform | django url', function (hooks) {
  setupTest(hooks);

  test('serializes', function (assert) {
    const transform = this.owner.lookup('transform:django-url');
    assert.strictEqual(
      transform.serialize('foo.bar/test'),
      'https://foo.bar/test'
    );
    assert.strictEqual(
      transform.serialize('https://foo.bar/test'),
      'https://foo.bar/test'
    );
  });
});
