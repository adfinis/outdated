import { visit } from '@ember/test-helpers';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { authenticateSession } from 'ember-simple-auth/test-support';
import { module, test } from 'qunit';

import { setupApplicationTest } from 'outdated/tests/helpers';

module('Acceptance | not-found', function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  test('Displays a 404 page for undefined routes if logged in', async function (assert) {
    await authenticateSession();
    await visit('/an-invalid-url');
    assert.dom('[data-test-not-found]').exists({ count: 1 });
  });
});
