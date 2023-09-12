import { visit, currentURL, click } from '@ember/test-helpers';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { authenticateSession } from 'ember-simple-auth/test-support';
import { module, test } from 'qunit';

import { setupApplicationTest } from 'outdated/tests/helpers';

module('Acceptance | projects', function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  test('Project clickable and link is correct', async function (assert) {
    const project = await this.server.create('project', 'withVersions');

    await authenticateSession();
    await visit('/');

    assert.strictEqual(currentURL(), '/');

    await click(`[data-test-project-link="${project.id}"]`);

    assert.strictEqual(currentURL(), `/projects/${project.id}`);

    assert
      .dom('[data-test-repo-link]')
      .hasProperty('href', `${project.repoProtocol}://${project.repo}`);

    assert
      .dom('tbody>tr')
      .exists({ count: project.versionedDependencies.models.length });
  });
});
