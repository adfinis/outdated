import { module, test } from 'qunit';
import { visit, currentURL, click } from '@ember/test-helpers';
import { setupApplicationTest } from 'outdated/tests/helpers';
import { setupMirage } from 'ember-cli-mirage/test-support';

module('Acceptance | projects', function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  test('Project clickable and link is correct', async function (assert) {
    const project = await this.server.create('project', 'withVersions');
    await visit('/');

    assert.strictEqual(currentURL(), '/');

    await click(`[data-test-project-link="${project.id}"]`);

    assert.strictEqual(currentURL(), `/projects/${project.id}`);

    assert.dom('[data-test-repo-link]').hasProperty('href', project.repo);
  });
});
