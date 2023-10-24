import { render, settled } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';
import { setupMirage } from 'ember-cli-mirage/test-support';
import { module, test } from 'qunit';

import { setupRenderingTest } from 'outdated/tests/helpers';
module('Integration | Component | project-detailed', function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test('it renders correctly', async function (assert) {
    const project = await this.server.create('project', 'withVersions');
    const store = this.owner.lookup('service:store');

    this.project = await store.findRecord('project', project.id, {
      include:
        'versionedDependencies,versionedDependencies.releaseVersion,versionedDependencies.releaseVersion.dependency',
    });

    await render(hbs`<ProjectDetailed @project={{this.project}} />`);

    assert.dom('[data-test-project-name]').hasText(this.project.name);
    assert
      .dom('[data-test-repo-link]')
      .hasProperty('href', this.project.repoURL);

    assert
      .dom('tbody>tr')
      .exists({ count: this.project.versionedDependencies.length });

    this.project.versionedDependencies = [];
    await settled();

    assert.dom('[data-test-versioned-dependencies-none]').exists();
  });
});
